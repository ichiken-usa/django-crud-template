import django_filters
from django.db import models

from .models import Item


class OrderingFilter(django_filters.filters.OrderingFilter):
    """ソートの表示変更"""
    descending_fmt = '%s （Descending）'


class ItemFilterSet(django_filters.FilterSet):
    """
    django-filter 構成クラス
    https://django-filter.readthedocs.io/en/latest/ref/filterset.html
    """

    # 検索フォームの並び順の設定
    order_by = OrderingFilter(
        initial='Created by',
        fields=(
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
        ),
        field_labels={
            'created_at': 'Created at',
            'updated_at': 'Updated at',
        },
        label='Sort order'
    )

    class Meta:
        model = Item

        # 検索に表示しない項目の設定
        exclude = ['created_at', 'updated_by', 'updated_at', ]
        
        # 文字列検索を部分一致に変更
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.TextField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }
