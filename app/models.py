from django.db import models
from django.core import validators
from django.utils import timezone
import uuid as uuid_lib

from users.models import User


class Area(models.Model):
    """
    エリアのテーブル
    """
    id = models.UUIDField(default=uuid_lib.uuid4,primary_key=True, editable=False)
    name = models.CharField(max_length=5, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        リストボックスやAdmin画面での表示
        """
        return self.name

    class Meta:
        """
        Admin画面でのタイトル表示
        """
        verbose_name = 'Area'
        verbose_name_plural = 'M Area'
        ordering = ['name'] # ソートの指定


class PrimaryCategory(models.Model):
    """
    親カテゴリ
    """
    id = models.UUIDField(default=uuid_lib.uuid4,primary_key=True, editable=False)
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        リストボックスやAdmin画面での表示
        """
        return self.name

    class Meta:
        """
        Admin画面でのタイトル表示
        """
        verbose_name = 'Primary categories'
        verbose_name_plural = 'M Primary categories'
        ordering = ['name']


class Category(models.Model):
    """
    カテゴリテーブル
    """
    id = models.UUIDField(default=uuid_lib.uuid4,primary_key=True, editable=False)
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    primary_category = models.ForeignKey(
        PrimaryCategory, 
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        リストボックスやAdmin画面での表示
        """
        return f'[{self.primary_category}] {self.code} : {self.name}'


    class Meta:
        """
        Admin画面でのタイトル表示
        """
        verbose_name = 'Categories'
        verbose_name_plural = 'M Categories'
        ordering = ['primary_category','code']


class Item(models.Model):
    """
    入力データフィールド定義クラス
    https://docs.djangoproject.com/ja/4.0/ref/models/fields/
    """

    # idは意図しないところで表示処理に使われておりUUIDやULIDにするとエラーになる。
    # 使用箇所がわかるまではデフォルトIDを使用。

    # Subject
    subject = models.CharField(
        verbose_name='Subject',
        max_length=32,
    )

    # Area 
    area = models.ForeignKey(
        Area,
        verbose_name='Area',
        on_delete=models.PROTECT
    )

    # Category
    category = models.ForeignKey(
        Category,
        verbose_name='Category',
        on_delete=models.PROTECT
    )

    # Sample int 入力範囲1~100
    sample_int = models.IntegerField(
        verbose_name='Sample int',
        blank=True,
        null=True,
        validators=[validators.MinValueValidator(1), validators.MaxValueValidator(100)]
    )

    # Sample float
    sample_float = models.FloatField(
        verbose_name='Sample float',
        blank=True,
        null=True
    )

    # Comment 200文字まで
    remarks = models.TextField(
        verbose_name='Repair details or Remarks (Max length 200)',
        blank=True,
        null=True,
        max_length=200,
    )

    # 作成者(ユーザー)
    created_by = models.ForeignKey(
        User,
        verbose_name='Created by',
        blank=True,
        null=True,
        related_name='CreatedBy',
        on_delete=models.PROTECT,
        editable=False,
    )

    # 作成時間
    created_at = models.DateTimeField(
        verbose_name='Created at',
        blank=True,
        null=True,
        editable=False,
    )

    # 更新者(ユーザー)
    updated_by = models.ForeignKey(
        User,
        verbose_name='Updated by',
        blank=True,
        null=True,
        related_name='UpdatedBy',
        on_delete=models.PROTECT,
        editable=False,
    )

    # 更新時間
    updated_at = models.DateTimeField(
        verbose_name='Updated at',
        blank=True,
        null=True,
        editable=False,
    )

    def __str__(self):
        """
        リストボックスやAdmin画面での表示
        """
        return self.subject

    class Meta:
        """
        Admin画面でのタイトル表示
        """
        verbose_name = 'Items'
        verbose_name_plural = 'D Items'


