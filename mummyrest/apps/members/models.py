import uuid
import math
import os

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from mummyrest.apps.utils import constants as const
from django.contrib.auth.hashers import make_password


class MembersManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, password=const.DEFAULT_PASSWORD, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, password=const.DEFAULT_PASSWORD, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(password, **extra_fields)

    def create_superuser(self, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(password, **extra_fields)


class Member(AbstractBaseUser):
    password = models.CharField(max_length=128)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    depth = models.PositiveIntegerField(default=0)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    channel = models.UUIDField(unique=True, default=uuid.uuid4,
                               editable=False, db_index=True)
    mummy_money = models.FloatField(default=0)
    start_week = models.ForeignKey('members.Week', on_delete=models.CASCADE, null=True)
    map_tree = models.TextField(blank=True)
    innocence = models.FloatField(default=0)
    experience = models.FloatField(default=0)
    charisma = models.FloatField(default=0)

    objects = MembersManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = []

    class Meta:
        abstract = False
        db_table = 'member'

    def __str__(self):
        return str(self.id)

    @property
    def is_rich(self):
        return self.money > float(os.getenv(const.MINIMUN_KEY, const.DEFAULT_MINIMUM))

    @property
    def recruit_probability(self):
        return self.innocence * (1 - self.experience)

    @property
    def max_weeks_without_money(self):
        return math.floor((1 - self.innocence) * self.experience * self.charisma * 10)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password


class Week(models.Model):
    new_members = models.PositiveIntegerField(default=0)
    leave_members = models.PositiveIntegerField(default=0)
    population = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'week'
