from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import transaction, IntegrityError
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

class MemberManager(BaseUserManager):
    def create_user(self, sid, name, email, password=None, **extra_fields):
        if not sid:
            raise ValueError("학번을 입력해주세요.")
        if not name:
            raise ValueError("이름을 입력해주세요.")
        if not email:
            raise ValueError("이메일이 입력되지 않았습니다.")
        
        # username이 명시적으로 들어오지 않았다면 sid로 설정
        if 'username' not in extra_fields:
            extra_fields['username'] = str(sid)
            
        if not password:
            password = str(sid)
            
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
        # 슈퍼유저도 username이 필수이므로 설정
        extra_fields.setdefault("username", str(sid))
        return self.create_user(sid, name, email, password, **extra_fields)
        
class Member(AbstractUser, PermissionsMixin):
    sid = models.IntegerField("학번", primary_key=True, unique=True)
    name = models.CharField("실명 또는 닉네임", max_length=100)
    email = models.EmailField("이메일", max_length=100, unique=True)
    
    # [추가] DB에 저장될 때 username이 없으면 sid를 복사해서 넣어줌 (Shell 작업 방지)
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = str(self.sid)
        super().save(*args, **kwargs)

    USERNAME_FIELD = "sid"
    REQUIRED_FIELDS = ["name", "email"]

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    groups = models.ManyToManyField('auth.Group', related_name="member_groups", blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name="member_user_permissions", blank=True)

    class Meta:
        db_table = "MEMBER"
        verbose_name = "회원"
        verbose_name_plural = "회원 목록"
        ordering = ['sid']
    
    objects = MemberManager()

    def __str__(self):
        return f"[{self.name}] ({self.sid})"