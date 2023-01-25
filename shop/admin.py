from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
from django.forms.models import BaseInlineFormSet
from django.utils.translation import gettext_lazy as _
from mptt.admin import DraggableMPTTAdmin

from shop import models


# Filter Spec
class RemovedOrderFilterSpec(SimpleListFilter):
    title = _('Removed Order')
    parameter_name = 'is_removed'

    def lookups(self, request, model_admin):
        return (
            ('1', _('Removed Order'),),
        )

    def queryset(self, request, queryset):
        kwargs = {
            '{}'.format(self.parameter_name): True,
        }
        if self.value() == '1':
            return queryset.filter(**kwargs)
        return queryset


class ProductCategoryFilterSpec(SimpleListFilter):
    title = _('category')
    parameter_name = 'category'

    def __init__(self, *args, **kwargs):
        self.categories = models.Category.objects \
            .filter(store__code='default', level__gt=0) \
            .order_by('tree_id', 'lft')
        super(ProductCategoryFilterSpec, self).__init__(*args, **kwargs)

    def lookups(self, request, model_admin):
        categories = ()

        for category in self.categories:
            categories += ((str(category.id), category.title),)

        return categories

    def queryset(self, request, queryset):
        kwargs = {
            '{}'.format(self.parameter_name): self.value(),
        }
        if self.value() in list(map(lambda x: str(x.id), self.categories)):
            return queryset.filter(**kwargs)
        return queryset


class VoucherProductCategoryFilterSpec(ProductCategoryFilterSpec):
    parameter_name = 'product__category'


class VoucherListPriceFilterSpec(SimpleListFilter):
    title = _('list price')
    parameter_name = 'product__subtitle'

    def __init__(self, *args, **kwargs):
        super(VoucherListPriceFilterSpec, self).__init__(*args, **kwargs)

    def lookups(self, request, model_admin):
        return (
            ('50만원', '50만원'),
            ('30만원', '30만원'),
            ('20만원', '20만원'),
            ('15만원', '15만원'),
            ('10만원', '10만원'),
            ('5만원', '5만원'),
            ('4만9천9백원', '4만9천9백원'),
            ('3만5천원', '3만5천원'),
            ('3만원', '3만원'),
            ('2만9천7백원', '2만9천7백원'),
            ('2만원', '2만원'),
            ('1만9천9백원', '1만9천9백원'),
            ('1만9천8백원', '1만9천8백원'),
            ('1만5천원', '1만5천원'),
            ('1만원', '1만원'),
            ('9천9백원', '9천9백원'),
            ('5천원', '5천원'),
            ('4천9백원', '4천9백원'),
            ('3천원', '3천원'),
            ('1천원', '1천원'),
            ('90일 정액권', '90일 정액권'),
            ('30일 정액권', '30일 정액권'),
        )

    def queryset(self, request, queryset):
        kwargs = {
            '{}'.format(self.parameter_name): self.value(),
        }
        if self.value():
            return queryset.filter(**kwargs)
        return queryset


# Formset and Inlines

class OrderPaymentInlineFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(OrderPaymentInlineFormset, self).__init__(*args, **kwargs)
        self.queryset = models.OrderPayment.objects \
            .select_related('order') \
            .filter(order=self.instance)

        self.initial = []

        for i in range(self.initial_form_count()):
            self.initial.append({})

        self.initial.append({'amount': self.instance.total_selling_price})


class OrderProductInlineFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(OrderProductInlineFormset, self).__init__(*args, **kwargs)
        self.queryset = models.OrderProduct.objects \
            .select_related('order') \
            .filter(order=self.instance)


class PurchaseOrderPaymentInlineFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(PurchaseOrderPaymentInlineFormset, self).__init__(*args, **kwargs)
        self.queryset = models.PurchaseOrderPayment.objects \
            .select_related('order') \
            .filter(order=self.instance)

        total = 0
        for p in self.queryset:
            total += p.amount

        self.initial = []

        for i in range(self.initial_form_count()):
            self.initial.append({})

        self.initial.append({'amount': self.instance.amount - total})


class OrderPaymentInline(admin.StackedInline):
    model = models.OrderPayment
    extra = 1
    formset = OrderPaymentInlineFormset
    fields = ('account', 'amount', 'received')
    ordering = ['-created']


class ProductInline(admin.TabularInline):
    model = models.ProductList.products.through
    extra = 1


class OrderProductVoucherInline(admin.TabularInline):
    model = models.OrderProductVoucher
    extra = 0
    fields = ('revoked', 'get_edit_link', 'code', 'remarks', 'order_no', 'created')
    readonly_fields = ('code', 'remarks', 'created')
    can_delete = False
    ordering = ['-created']


class NaverOrderProductVoucherInline(admin.TabularInline):
    model = models.NaverOrderProductVoucher
    extra = 0
    fields = ('revoked', 'get_edit_link', 'code', 'remarks', 'order_no', 'created')
    readonly_fields = ('code', 'remarks', 'created')
    can_delete = False


class OrderProductInline(admin.TabularInline):
    model = models.OrderProduct
    fields = ('get_edit_link', 'selling_price')
    readonly_fields = ('selling_price',)
    formset = OrderProductInlineFormset
    can_delete = False
    extra = 0


class PurchaseOrderPaymentInline(admin.StackedInline):
    model = models.PurchaseOrderPayment
    extra = 1
    formset = PurchaseOrderPaymentInlineFormset
    fields = ('account', 'amount')
    readonly_fields = ('created',)
    ordering = ['-created']


class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'theme', 'chunk_size', 'block_size')
    ordering = ['-created']


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'subtitle', 'stock', 'stock_quantity', 'minimum_stock_level', 'maximum_stock_level', 'status',
        'position', 'pg', 'naver_partner', 'naver_partner_title'
    )
    list_display_links = ('name', 'subtitle')
    list_filter = ('store__name', ProductCategoryFilterSpec, 'status', 'stock', 'naver_partner', 'pg')
    ordering = ['category__title', 'position']
    inlines = [ProductInline]


class ProductListAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'store')
    inlines = [ProductInline]
    exclude = ('products',)


class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'slug', 'discount_rate', 'pg', 'pg_discount_rate', 'store')
    list_filter = ('store__name', 'created')
    prepopulated_fields = {'slug': ('title',)}
    mptt_level_indent = 20
    ordering = ['tree_id', 'lft']


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'fullname', 'payment_method', 'status', 'created', 'is_removed')
    list_filter = ('payment_method', 'status', RemovedOrderFilterSpec,)
    date_hierarchy = 'created'
    search_fields = ('user__email',)
    fieldsets = (
        (_('Order Info'), {
            'fields': (
                'order_no', 'fullname', 'phone',
                'total_amount', 'payment_method', 'status', 'created', 'visible'
            )
        }),
        (_('Transaction Verification'), {
            'fields': (
                'suspicious',
                'phone_verified_status', 'document_verified',
                'date_joined', 'last_login_count', 'last_purchased', 'last_total',
                'max_price', 'average_price', 'total_order_count',
                'country', 'accept_language', 'user_agent', 'message'
            )
        }),
    )
    readonly_fields = (
        'order_no', 'fullname', 'total_list_price', 'payment_method', 'currency', 'created',
        'accept_language', 'user_agent', 'message'
    )
    inlines = [OrderProductInline, OrderPaymentInline]
    ordering = ['-created', ]

    def get_queryset(self, request):
        return super(OrderAdmin, self).get_queryset(request) \
            .select_related('user', 'user__profile', 'parent')


class VoucherAdmin(admin.ModelAdmin):
    list_display = ('status', 'created')
    list_select_related = ('product',)
    list_filter = ('status', VoucherProductCategoryFilterSpec, VoucherListPriceFilterSpec)
    search_fields = ('code',)
    date_hierarchy = 'created'
    fields = ('product_name_subtitle', 'product', 'code', 'remarks', 'status', 'created')
    readonly_fields = ('is_removed', 'created')
    inlines = [OrderProductVoucherInline, NaverOrderProductVoucherInline]
    order = ['-created']


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'subtitle', 'selling_price', 'quantity', 'created')
    list_display_links = ('name', 'subtitle')
    list_select_related = ('order', 'order__user')
    search_fields = ('order__order_no',)
    date_hierarchy = 'created'
    fields = ('order_no', 'name', 'code', 'list_price', 'selling_price', 'quantity')
    readonly_fields = ('order', 'name', 'code', 'list_price', 'selling_price', 'quantity')
    inlines = [OrderProductVoucherInline]
    order = ['-created']

    def get_queryset(self, request):
        return super(OrderProductAdmin, self).get_queryset(request) \
            .select_related('order', 'order__user')


class OrderProductVoucherAdmin(admin.ModelAdmin):
    list_display = ('revoked', 'code', 'remarks', 'created')
    list_display_links = ('code',)
    list_select_related = ('order_product', 'order_product__order')
    search_fields = ('order_product__order__order_no', 'code')
    list_filter = ('revoked',)
    fields = ('order_no', 'product_name_subtitle', 'code_truncated', 'remarks', 'created')
    readonly_fields = ('remarks', 'created',)
    order = ['-created']


class NaverOrderAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'fullname', 'payment_method', 'status', 'created', 'is_removed')
    list_filter = ('payment_method', 'status', RemovedOrderFilterSpec,)
    date_hierarchy = 'created'
    search_fields = ('fullname',)
    fields = (
        'order_no', 'fullname', 'phone',
        'total_list_price', 'total_selling_price', 'payment_method', 'status', 'message'
    )
    readonly_fields = (
        'order_no', 'fullname', 'phone',
        'total_list_price', 'total_selling_price', 'payment_method',  # 'status'
    )
    # inlines = [OrderProductInline, OrderPaymentInline]
    ordering = ['-created', ]


class NaverOrderProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'subtitle', 'selling_price', 'quantity', 'created')
    list_display_links = ('name', 'subtitle')
    list_select_related = ('order',)
    search_fields = ('order__order_no',)
    date_hierarchy = 'created'
    fields = ('order_no', 'name', 'code', 'list_price', 'selling_price', 'quantity')
    readonly_fields = ('order', 'name', 'code', 'list_price', 'selling_price', 'quantity')
    inlines = [NaverOrderProductVoucherInline]
    order = ['-created']

    def get_queryset(self, request):
        return super(NaverOrderProductAdmin, self).get_queryset(request) \
            .select_related('order')


class NaverOrderProductVoucherAdmin(admin.ModelAdmin):
    list_display = ('revoked', 'code', 'remarks', 'created')
    list_display_links = ('code',)
    list_select_related = ('order_product', 'order_product__order')
    search_fields = ('order_product__order__order_no', 'code')
    list_filter = ('revoked',)
    fields = ('order_no', 'product_name_subtitle', 'code_truncated', 'remarks', 'created')
    readonly_fields = ('remarks', 'created')
    order = ['-created']


class LegacyOrderAdmin(admin.ModelAdmin):
    pass


class LegacyOrderProductAdmin(admin.ModelAdmin):
    pass


class LegacyCustomerAdmin(admin.ModelAdmin):
    pass


class NaverAdvertisementLogAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'rank', 'campaign_type', 'media', 'query', 'ip_address', 'created')
    search_fields = ('keyword', 'ip_address')
    readonly_fields = ('keyword', 'rank', 'campaign_type', 'media', 'query',
                       'ip_address', 'ad_group', 'ad', 'keyword_id', 'user_agent')
    list_filter = ('campaign_type', 'media')
    date_hierarchy = 'created'
    ordering = ['-created']


class MileageLogAdmin(admin.ModelAdmin):
    list_display = ('mileage', 'created', 'order')
    list_select_related = ('user', 'user__profile', 'order')
    search_fields = ('user__email',)
    readonly_fields = ('is_removed', 'created')
    date_hierarchy = 'created'
    ordering = ['-created']
    raw_id_fields = ('user', 'order')


class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('title', 'bank_account', 'amount', 'paid', 'created')
    search_fields = ('bank_account', 'amount')
    readonly_fields = ('content', 'paid', 'is_removed', 'created')
    list_filter = ('paid',)
    date_hierarchy = 'created'
    ordering = ['-created']
    inlines = [PurchaseOrderPaymentInline, ]


admin.site.register(models.Store, StoreAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductList, ProductListAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderProduct, OrderProductAdmin)
admin.site.register(models.Voucher, VoucherAdmin)
admin.site.register(models.OrderProductVoucher, OrderProductVoucherAdmin)
admin.site.register(models.NaverOrder, NaverOrderAdmin)
admin.site.register(models.NaverOrderProduct, NaverOrderProductAdmin)
admin.site.register(models.NaverOrderProductVoucher, NaverOrderProductVoucherAdmin)
admin.site.register(models.LegacyCustomer, LegacyCustomerAdmin)
admin.site.register(models.LegacyOrder, LegacyOrderAdmin)
admin.site.register(models.LegacyOrderProduct, LegacyOrderProductAdmin)
admin.site.register(models.NaverAdvertisementLog, NaverAdvertisementLogAdmin)
admin.site.register(models.MileageLog, MileageLogAdmin)
admin.site.register(models.PurchaseOrder, PurchaseOrderAdmin)
