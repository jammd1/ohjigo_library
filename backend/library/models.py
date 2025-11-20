from django.db import models
from django.core.validators import RegexValidator
from members.models import Member
from manager.models import Manager
from django.utils import timezone

# -----------------------------------------------------------------------------
# 3. BOOK (물리적 도서)
# -----------------------------------------------------------------------------
class Book(models.Model):
    """
    물리적 도서 테이블 (BOOK)
    서가에 있는 개별 도서의 재고 및 상태 정보를 관리합니다.
    """
    class Status(models.TextChoices):
        AVAILABLE = 'AVAILABLE', '대출 가능'
        ON_LOAN = 'ON_LOAN', '대출 중'
        LOST = 'LOST', '분실'

    class Category(models.TextChoices):
        LITERATUR = 'Literatur', '문학'
        SPRACHWISSENSCHAFT = 'Sprachwissenschaft', '어학'
        GESCHICHTE = 'Geschichte', '역사'
        SOZIALWISSENSCHAFTEN = 'Sozialwissenschaften', '사회과학'
        SONSTIGES = 'Sonstiges', '기타'

    # book_id를 PK로, call_number를 Unique 필드로 사용하는 것이 가장 안정적입니다.
    book_id = models.AutoField("도서 고유 ID (바코드)", primary_key=True)
    call_number = models.CharField("고유 청구기호", max_length=50, unique=True)
    title = models.CharField("도서 제목", max_length=255)
    author = models.CharField("저자", max_length=255, null=True, blank=True)
    status = models.CharField(
        "현재 상태", max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    
    # 도서 위치: 'A~D-(숫자)' 형식 (예: A-4, B-12, C-3, D-25)
    location_validator = RegexValidator(
        regex=r'^[A-D]-\d+$',
        message="도서 위치는 'A~D-(숫자)' 형식이어야 합니다. (예: A-4)"
    )
    location = models.CharField(
        "도서 위치", 
        max_length=10, 
        validators=[location_validator],
        null=True,
        blank=True,
        help_text="도서 위치 형식: A~D-(숫자) (예: A-4)"
    )
    
    # 분야: 5가지 선택지
    category = models.CharField(
        "분야", 
        max_length=20, 
        choices=Category.choices,
        default=Category.SONSTIGES
    )

    # ForeignKey 필드: 관리자가 삭제되어도 도서 기록은 남아야 하므로 on_delete=models.SET_NULL 사용
    registrar_manager = models.ForeignKey(
        Manager, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name="최초 등록 관리자", 
        related_name="registered_books"  # 역참조 시 사용할 이름
    )
    registration_date = models.DateTimeField("최초 등록 시각", auto_now_add=True)
    
    modification_manager = models.ForeignKey(
        Manager, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="최종 수정 관리자", 
        related_name="modified_books"
    )
    modification_date = models.DateTimeField(
        "최종 수정 시각", null=True, blank=True)

    class Meta:
        db_table = 'BOOK'
        verbose_name = '도서'
        verbose_name_plural = '도서 목록'
        ordering = ['title', 'call_number'] # 제목, 청구기호 순으로 정렬

    def __str__(self):
        return f"{self.title} ({self.call_number})"

    def save(self, *args, **kwargs):
        # 객체가 데이터베이스에 이미 존재하는 경우(업데이트)에만 최종 수정 시각을 업데이트합니다.
        if self.pk:
            self.modification_date = timezone.now()
        super(Book, self).save(*args, **kwargs)

# -----------------------------------------------------------------------------
# 4. LOAN (대출 기록 트랜잭션)
# -----------------------------------------------------------------------------
class Loan(models.Model):
    """
    대출 기록 트랜잭션 테이블 (LOAN)
    도서 대출 및 반납에 대한 모든 기록을 저장합니다.
    """
    loan_id = models.AutoField("대출 트랜잭션 고유 ID", primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name="대출 회원")
    
    # 대출 기록이 있는 도서는 삭제할 수 없도록 on_delete=models.PROTECT 사용
    book = models.ForeignKey(Book, on_delete=models.PROTECT, verbose_name="대출 도서")
    
    loan_date = models.DateTimeField("대출 시작 시각", auto_now_add=True)
    due_date = models.DateTimeField("반납 예정일")
    return_date = models.DateTimeField("실제 반납 완료 시각", null=True, blank=True)
    
    loan_manager = models.ForeignKey(
        Manager, on_delete=models.SET_NULL, null=True, verbose_name="업무 처리 관리자")
    
    @property
    def overdue_days(self):
        """
        연체일수를 동적으로 계산합니다.
        - 반납 완료 시: 반납일 - 반납 예정일
        - 대출 중일 시: 오늘 날짜 - 반납 예정일 (연체된 경우)
        """
        if self.return_date:
            # 반납이 완료된 경우
            if self.return_date.date() > self.due_date.date():
                return (self.return_date.date() - self.due_date.date()).days
            return 0
        else:
            # 아직 대출 중인 경우
            if timezone.now().date() > self.due_date.date():
                return (timezone.now().date() - self.due_date.date()).days
            return 0

    class Meta:
        db_table = 'LOAN'
        verbose_name = '대출 기록'
        verbose_name_plural = '대출 기록 목록'
        ordering = ['-loan_date'] # 최신 대출이 먼저 오도록 정렬

    def __str__(self):
        return f"대출 ID {self.loan_id} ({self.member.sid} -> {self.book.title})"

# -----------------------------------------------------------------------------
# 5. NOTICE (공지사항)
# -----------------------------------------------------------------------------
class Notice(models.Model):
    """
    공지사항 테이블 (NOTICE)
    관리자가 작성하는 공지사항 게시글을 관리합니다.
    """
    notice_id = models.AutoField("공지사항 고유 ID", primary_key=True)
    
    # 작성한 관리자가 삭제되어도 공지사항은 남도록 on_delete=models.SET_NULL 사용
    manager = models.ForeignKey(
        Manager, on_delete=models.SET_NULL, null=True, verbose_name="작성 관리자"
        )
    title = models.CharField("게시글 제목", max_length=255)
    content = models.TextField("게시글 본문 내용")
    post_date = models.DateTimeField("게시글 최초 작성일", auto_now_add=True)
    view_count = models.IntegerField("조회수", default=0)

    class Meta:
        db_table = 'NOTICE'
        verbose_name = '공지사항'
        verbose_name_plural = '공지사항 목록'
        ordering = ['-post_date'] # 최신 글이 먼저 오도록 정렬 및 리스트 반환
        

    def __str__(self):
        return self.title
