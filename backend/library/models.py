from django.db import models
from django.core.validators import RegexValidator
from members.models import Member
from manager.models import Manager
from django.utils import timezone
from datetime import timedelta # ★ 날짜 계산을 위해 추가

# -----------------------------------------------------------------------------
# 3. BOOK (물리적 도서)
# -----------------------------------------------------------------------------
class Book(models.Model):
    """
    물리적 도서 테이블 (BOOK)
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

    class Language(models.TextChoices):
        KOREAN = 'KR', '한국어'
        GERMAN = 'DE', '독일어'
        ENGLISH = 'EN', '영어'
        OTHER = 'ETC', '기타'

    book_id = models.AutoField("도서 고유 ID (바코드)", primary_key=True)
    call_number = models.CharField("고유 청구기호", max_length=50, unique=True)
    title = models.CharField("도서 제목", max_length=255)
    author = models.CharField("저자", max_length=255, null=True, blank=True)
    status = models.CharField(
        "현재 상태", max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    language = models.CharField(
        "언어", max_length=5, choices=Language.choices, default=Language.GERMAN
    )
    
    location_validator = RegexValidator(
        regex=r'^[A-D]\d-\d+$',
        message="도서 위치는 'A~D(숫자)-(숫자)' 형식이어야 합니다. (예: A1-4)"
    )
    location = models.CharField(
        "도서 위치", 
        max_length=10, 
        validators=[location_validator],
        null=True, blank=True,
        help_text="도서 위치 형식: A~D(숫자)-(숫자) (예: A1-4)"
    )
    
    category = models.CharField(
        "분야", max_length=20, choices=Category.choices, default=Category.SONSTIGES
    )

    registrar_manager = models.ForeignKey(
        Manager, on_delete=models.SET_NULL, null=True, verbose_name="최초 등록 관리자", related_name="registered_books"
    )
    registration_date = models.DateTimeField("최초 등록 시각", auto_now_add=True)
    
    modification_manager = models.ForeignKey(
        Manager, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="최종 수정 관리자", related_name="modified_books"
    )
    modification_date = models.DateTimeField("최종 수정 시각", null=True, blank=True)

    class Meta:
        db_table = 'BOOK'
        verbose_name = '도서'
        verbose_name_plural = '도서 목록'
        ordering = ['title', 'call_number']

    def __str__(self):
        return f"{self.title} ({self.call_number})"

    def save(self, *args, **kwargs):
        if self.pk:
            self.modification_date = timezone.now()
        super(Book, self).save(*args, **kwargs)

# -----------------------------------------------------------------------------
# 4. LOAN (대출 기록 트랜잭션)
# -----------------------------------------------------------------------------
class Loan(models.Model):
    """
    대출 기록 트랜잭션 테이블 (LOAN)
    """
    loan_id = models.AutoField("대출 트랜잭션 고유 ID", primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name="대출 회원")
    book = models.ForeignKey(Book, on_delete=models.PROTECT, verbose_name="대출 도서")
    
    loan_date = models.DateTimeField("대출 시작 시각", auto_now_add=True)
    
    # ★ [변경] blank=True 추가: 관리자가 입력 안 해도 save() 함수에서 자동으로 채워주기 위해
    due_date = models.DateTimeField("반납 예정일", blank=True, null=True)
    return_date = models.DateTimeField("실제 반납 완료 시각", null=True, blank=True)
    
    loan_manager = models.ForeignKey(
        Manager, on_delete=models.SET_NULL, null=True, verbose_name="업무 처리 관리자")
    
    @property
    def overdue_days(self):
        if self.return_date:
            if self.return_date.date() > self.due_date.date():
                return (self.return_date.date() - self.due_date.date()).days
            return 0
        else:
            if self.due_date and timezone.now().date() > self.due_date.date():
                return (timezone.now().date() - self.due_date.date()).days
            return 0

    class Meta:
        db_table = 'LOAN'
        verbose_name = '대출 기록'
        verbose_name_plural = '대출 기록 목록'
        ordering = ['-loan_date']

    def __str__(self):
        return f"대출 ID {self.loan_id} ({self.member.sid} -> {self.book.title})"

    # ★★★ [핵심 기능] 자동화 로직 추가 ★★★
    def save(self, *args, **kwargs):
        # 1. 신규 대출인 경우 (ID가 생성되기 전)
        if not self.pk:
            # (1) 반납일 자동 계산 로직
            # Member 모델의 Role 상수를 사용합니다.
            if self.member.role == Member.Role.PROFESSOR:
                # 교수: 3개월 (90일)
                days = 90
            elif self.member.role == Member.Role.GRADUATE:
                # 대학원생: 1개월 (30일)
                days = 30
            else:
                # 학부생/졸업생/기타: 2주 (14일)
                days = 14
            
            # timezone.now()는 현재 시각
            self.due_date = timezone.now() + timedelta(days=days)

            # (2) 도서 상태를 '대출 중'으로 변경
            self.book.status = Book.Status.ON_LOAN
            self.book.save()

        # 2. 반납일(return_date)이 기록된 경우
        if self.return_date:
            # 도서 상태를 '대출 가능'으로 복구
            self.book.status = Book.Status.AVAILABLE
            self.book.save()

        super().save(*args, **kwargs)

# -----------------------------------------------------------------------------
# 5. NOTICE (공지사항)
# -----------------------------------------------------------------------------
class Notice(models.Model):
    notice_id = models.AutoField("공지사항 고유 ID", primary_key=True)
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
        ordering = ['-post_date'] 

    def __str__(self):
        return self.title