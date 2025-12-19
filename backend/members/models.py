from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import transaction, IntegrityError
import logging
from django.utils import timezone

# Member 생성 관리자 클래스
logger = logging.getLogger(__name__)

class MemberManager(BaseUserManager):
    def create_user(self, sid, name, email, password=None, **extra_fields):
        if not sid:
            raise ValueError("학번을 입력해주세요.")
        if not name:
            raise ValueError("이름을 입력해주세요.")
        if not email:
            raise ValueError("이메일이 입력되지 않았습니다.")
        
        if not password:
            password = str(sid)  # SID를 문자열로 변환하여 비밀번호로 설정
            
        extra_fields.setdefault('member_last_activity', timezone.now())
        
        try:
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
        except IntegrityError:
            logger.warning(f"이미 존재하는 학번 또는 이메일입니다: 학번={sid}, 이메일={email}")
            raise ValueError("이미 존재하는 학번 또는 이메일입니다.")
        except Exception as e:
            logger.error(f"사용자(sid:{sid}) 생성 중 오류 발생: {e}", exc_info=True)
            raise e
        
    def create_superuser(self, sid, name, email, password=None, **extra_fields):
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
    
    sid = models.IntegerField("학번", primary_key=True, unique=True)
    name = models.CharField("실명 또는 닉네임", max_length=100)
    email = models.EmailField("이메일", max_length=100, unique=True)
    status = models.CharField("계정 상태", max_length=20, choices=Status.choices, default=Status.ACTIVE)
    role = models.CharField("신분", max_length=20, choices=Role.choices, default=Role.UNDERGRADUATE)
    member_last_activity = models.DateTimeField("최종 활동 시각", auto_now=True)
    join_date = models.DateTimeField("최초 회원가입 시각", auto_now_add=True)
    USERNAME_FIELD = sid
    REQUIRED_FIELDS = ["name", "email"]

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # ★ [중요] Django 기본 User 모델과의 충돌 방지를 위한 설정
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="member_groups",  # 역참조 이름 변경
        related_query_name="member",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="member_user_permissions",  # 역참조 이름 변경
        related_query_name="member",
    )

    class Meta:
        db_table = "MEMBER"
        verbose_name = "회원"
        verbose_name_plural = "회원 목록"
        ordering = ['sid']
    
    objects = MemberManager()

    USERNAME_FIELD = "sid"
    REQUIRED_FIELDS = ["name", "email"]

    def __str__(self):
        return f"[{self.get_role_display()}] {self.name} ({self.sid})"