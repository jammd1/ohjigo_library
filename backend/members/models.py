from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import transaction, IntegrityError
import logging
from django.utils import timezone

# Member 생성 관리자 클래스
logger = logging.getLogger(__name__)

class MemberManager(BaseUserManager):
    def create_user(self, sid, name, email, password=None, **extra_fields):
        # --- 필수 입력값 검증 ---
        if not sid:
            raise ValueError("학번을 입력해주세요.")
        if not name:
            raise ValueError("이름을 입력해주세요.")
        if not email:
            raise ValueError("이메일을 입력해주세요.")
        # --- 비밀번호 정책 --- 
        if not password:
            password = sid  # 비밀번호가 제공되지 않으면 SID로 설정
        if 'member_last_activity' not in extra_fields:
            # auto_now_add 필드는 객체 생성 시점에 바로 접근이 어려우므로
            # timezone.now()로 명시적 값 생성
            extra_fields['member_last_activity'] = timezone.now()
        try:
            # --- 트랜젝션 ---
            with transaction.atomic():
                email = self.normalize_email(email)
                user = self.model(
                    sid=sid, 
                    name=name, 
                    email=email, 
                    **extra_fields
                )
                user.set_password(password)
                user.save(using=self._db)
                return user
        # --- 중복 데이터 예외 처리 ---
        except IntegrityError:
            # sid 또는 email이 이미 DB에 존재하는 경우 logging
            logger.warning(f"이미 존재하는 학번 또는 이메일입니다: 학번={sid}, 이메일={email}")
            raise ValueError("이미 존재하는 학번 또는 이메일입니다.")
        
        except Exception as e:
            # 그 외 모든 에러에 대한 logging
            logger.error(f"사용자(sid:{sid}) 생성 중 오류 발생: {e}", exc_info=True)
            raise e
        
    def create_superuser(self, sid, name, email, password=None, **extra_fields):
        # default로 is_staff, is_superuser를 True로 설정
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
                raise ValueError("슈퍼유저는 is_staff=True 여야 합니다.")
        if extra_fields.get("is_superuser") is not True:
                raise ValueError("슈퍼유저는 is_superuser=True 여야 합니다.")
        return self.create_user(sid, name, email, password, **extra_fields)
        
class Member(AbstractUser, PermissionsMixin):
    """
    회원정보 테이블 (MEMBER)
    시스템 사용자의 로그인 정보 및 개인정보를 관리하는 클래스
    """
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "활성"
        DORMANT = "DORMANT", "휴면"
        WITHDRAWN = "WITHDRAWN", "탈퇴"
        SUSPENDED = "SUSPENDED", "정지"

    class Role(models.TextChoices):
        PROFESSOR = "PROFESSOR", "교수"
        GRADUATE = "GRADUATE", "대학원생"
        UNDERGRADUATE = "UNDERGRADUATE", "학부생/졸업생"
    
    sid = models.IntegerField("학번", primary_key=True, unique=True)  # 학번 (PK)
    name = models.CharField("실명 또는 닉네임", max_length=100) # 이름
    email = models.EmailField("이메일", max_length=100, unique=True) # 이메일
    status = models.CharField("계정 상태", max_length = 20, choices=Status.choices, default=Status.ACTIVE) # 계정 상태
    role = models.CharField("신분", max_length=20, choices=Role.choices, default=Role.UNDERGRADUATE)
    member_last_activity = models.DateTimeField("최종 활동 시각", auto_now=True) # 최종 활동 시각
    join_date = models.DateTimeField("최초 회원가입 시각", auto_now_add = True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    username = None

    class Meta:
        db_table = "MEMBER" # 테이블
        verbose_name = "회원" # 관리자 페이지에서 사용할 단수 이름
        verbose_name_plural = "회원 목록" # 관리자 페이지에서 사용할 복수 이름
        ordering = ['sid'] # 기본 정렬 기준(학번 오름차순)
    
    objects = MemberManager()

    USERNAME_FIELD = "sid"  # 로그인 시 사용할 필드
    REQUIRED_FIELDS = ["name", "email"]  # superuser 생성 시 필요한 필드

    def __str__(self):
        return f"[{self.get_role_display()}] {self.name} ({self.sid})"