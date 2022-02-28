from django.contrib import admin

from .models import Item, Area, Category, PrimaryCategory

# デコレータにクラス追加すればAdmin画面に表示される
@admin.register(Item, Area, Category, PrimaryCategory)
class ItemAdmin(admin.ModelAdmin):
    """
    Admin画面の表示設定
    https://docs.djangoproject.com/ja/4.0/ref/contrib/admin/
    """
    class Meta:
        pass

