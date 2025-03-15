from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from unfold.widgets import UnfoldAdminSelectWidget, UnfoldAdminTextInputWidget
from .models import (
    ProductCategory,
    ProductFamily,
    ProductModel,
    ChipOption,
    ProductImage,
)
from unfold.decorators import display
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _
from products.templatetags.currency_filters import format_currency
from django.utils.html import strip_tags

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from django_celery_beat.admin import ClockedScheduleAdmin as BaseClockedScheduleAdmin
from django_celery_beat.admin import CrontabScheduleAdmin as BaseCrontabScheduleAdmin
from django_celery_beat.admin import PeriodicTaskAdmin as BasePeriodicTaskAdmin
from django_celery_beat.admin import PeriodicTaskForm, TaskSelectWidget

admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)

admin.site.unregister(User)
admin.site.unregister(Group)
@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


@admin.register(ProductFamily)
class ProductFamilyAdmin(ModelAdmin):
    list_display = ["eng_name", "marketing_name"]
    search_fields = ["eng_name", "marketing_name"]

class StockStatus(TextChoices):
    IN_STOCK = "Còn hàng", _("Còn hàng")
    OUT_OF_STOCK = "Hết hàng", _("Hết hàng")
    # Register your models here.
@admin.register(ProductCategory)
class ProductCategoryAdmin(ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


class ChipOptionInline(TabularInline):
    model = ChipOption
    extra = 1
    tab = True


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1
    tab = True


@admin.register(ProductModel)
class ProductModelAdmin(ModelAdmin):
    list_display = [
        "product_marketing_name", 
        "model_code", 
        "display_name",
        "price_formatted",
        "promotion_price_formatted",
        "stock_status_text",
        "options",
    ]
    search_fields = [
        "product_family__marketing_name", 
        "model_code", 
        "display_name",
        "chip_options__chip_name",
        "product_family__category__name"
    ]
    list_filter = ["stock_status","product_family__category__name"]
    autocomplete_fields = ["product_family"]
    inlines = [ProductImageInline, ChipOptionInline]
    autocomplete_fields = ["product_family"]
    def product_marketing_name(self, obj):
        return obj.product_family.marketing_name
    product_marketing_name.short_description = "Tên thương mại"
    
    
    @display(
        description="Kho hàng",
        label = {
            StockStatus.IN_STOCK: "info",  # blue
            StockStatus.OUT_OF_STOCK: "danger",  # red
        }
    )
    def stock_status_text(self, obj):
        return "Còn hàng" if obj.stock_status == "inStock" else "Hết hàng"
    stock_status_text.short_description = "Kho hàng"
    
    @display(
        description="Biến thẻ",
        label = True
    )
    def options(self, obj):
        return ", ".join([option.chip_name for option in obj.chip_options.all()])
    
    @display(
        description="Giá",
    )
    def price_formatted(self, obj):
        return format_currency(obj.price)
    
    @display(
        description="Giá khuyến mãi",
    )
    def promotion_price_formatted(self, obj):
        return format_currency(obj.promotion_price)
    
    @display(
        description="Sales text",
    )
    def sales_text_display(self, obj):
        return strip_tags(obj.sales_text) if obj.sales_text else "Không có"
    
    



class UnfoldTaskSelectWidget(UnfoldAdminSelectWidget, TaskSelectWidget):
    pass


class UnfoldPeriodicTaskForm(PeriodicTaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task"].widget = UnfoldAdminTextInputWidget()
        self.fields["regtask"].widget = UnfoldTaskSelectWidget()


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(BasePeriodicTaskAdmin, ModelAdmin):
    form = UnfoldPeriodicTaskForm


@admin.register(IntervalSchedule)
class IntervalScheduleAdmin(ModelAdmin):
    pass


@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(BaseCrontabScheduleAdmin, ModelAdmin):
    pass


@admin.register(SolarSchedule)
class SolarScheduleAdmin(ModelAdmin):
    pass

@admin.register(ClockedSchedule)
class ClockedScheduleAdmin(BaseClockedScheduleAdmin, ModelAdmin):
    pass