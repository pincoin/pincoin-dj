import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from model_utils import Choices
from model_utils import models as model_utils_models
from model_utils.fields import StatusField
from mptt.fields import TreeForeignKey

from common import models as common_models


def upload_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/blog/<today>/<uuid>.<ext>
    return f"shop/{now().strftime('%Y-%m-%d')}/{uuid.uuid4()}.{filename.split('.')[-1]}"


class Store(model_utils_models.TimeStampedModel):
    STATUS_CHOICES = Choices(
        (0, 'enabled', _('enabled')),
        (1, 'disabled', _('disabled')),
        (2, 'maintenance', _('maintenance'))
    )

    name = models.CharField(
        verbose_name=_('store name'),
        max_length=255,
    )

    code = models.SlugField(
        verbose_name=_('store code'),
        help_text=_('A short label containing only letters, numbers, underscores or hyphens for URL'),
        max_length=255,
        unique=True,
        allow_unicode=True,
    )

    theme = models.CharField(
        verbose_name=_('theme'),
        max_length=250,
        default='default',
    )

    phone = models.CharField(
        verbose_name=_('phone number'),
        max_length=16,
        blank=True,
        null=True,
    )

    phone1 = models.CharField(
        verbose_name=_('phone number1'),
        max_length=16,
        blank=True,
        null=True,
    )

    kakao = models.CharField(
        verbose_name=_('kakao ID'),
        max_length=16,
        blank=True,
        null=True,
    )

    bank_account = models.TextField(
        verbose_name=_('bank accounts'),
        blank=True,
    )

    escrow_account = models.TextField(
        verbose_name=_('escrow'),
        blank=True,
    )

    chunk_size = models.PositiveIntegerField(
        verbose_name=_('pagination chunk size'),
        default=10,
    )

    block_size = models.PositiveIntegerField(
        verbose_name=_('pagination block size'),
        default=10,
    )

    signup_open = models.BooleanField(
        verbose_name=_('signup open'),
        default=True,
    )

    under_attack = models.BooleanField(
        verbose_name=_('under attack'),
        default=False,
    )

    class Meta:
        verbose_name = _('store')
        verbose_name_plural = _('stores')

    def __str__(self):
        return self.name


class Category(common_models.AbstractCategory):
    store = models.ForeignKey(
        'shop.Store',
        verbose_name=_('store'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    thumbnail = ThumbnailerImageField(
        verbose_name=_('thumbnail'),
        upload_to=upload_directory_path,
        blank=True,
    )

    description = models.TextField(
        verbose_name=_('description'),
        blank=True,
    )

    description1 = models.TextField(
        verbose_name=_('description1'),
        blank=True,
    )

    discount_rate = models.DecimalField(
        verbose_name=_('discount rate'),
        max_digits=3,
        decimal_places=2,
    )

    pg = models.BooleanField(
        verbose_name=_('PG'),
        default=False,
    )

    pg_discount_rate = models.DecimalField(
        verbose_name=_('PG discount rate'),
        max_digits=3,
        decimal_places=2,
        default=0,
    )

    naver_search_tag = models.CharField(
        verbose_name=_('naver search tag'),
        max_length=99,
        blank=True,
    )

    naver_brand_name = models.CharField(
        verbose_name=_('naver brand name'),
        max_length=59,
        blank=True,
    )

    naver_maker_name = models.CharField(
        verbose_name=_('naver maker name'),
        max_length=59,
        blank=True,
    )

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.title


class Product(model_utils_models.SoftDeletableModel, model_utils_models.TimeStampedModel):
    STATUS_CHOICES = Choices(
        (0, 'enabled', _('enabled')),
        (1, 'disabled', _('disabled')),
    )

    STOCK_CHOICES = Choices(
        (0, 'sold_out', _('sold out')),
        (1, 'in_stock', _('in stock')),
    )

    name = models.CharField(
        verbose_name=_('product name'),
        max_length=255,
    )

    subtitle = models.CharField(
        verbose_name=_('product subtitle'),
        max_length=255,
        blank=True,
    )

    code = models.SlugField(
        verbose_name=_('product code'),
        help_text=_('A short label containing only letters, numbers, underscores or hyphens for URL'),
        max_length=255,
        unique=True,
        allow_unicode=True,
    )

    # Max = 999,999,999.99
    list_price = models.DecimalField(
        verbose_name=_('list price'),
        max_digits=11,
        decimal_places=2,
    )

    selling_price = models.DecimalField(
        verbose_name=_('selling price'),
        max_digits=11,
        decimal_places=2,
    )

    pg = models.BooleanField(
        verbose_name=_('PG'),
        default=False,
    )

    pg_selling_price = models.DecimalField(
        verbose_name=_('payment gateway selling price'),
        max_digits=11,
        decimal_places=2,
        default=0,
    )

    description = models.TextField(
        verbose_name=_('description'),
        blank=True,
    )

    store = models.ForeignKey(
        'shop.Store',
        verbose_name=_('store'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    category = TreeForeignKey(
        'shop.Category',
        verbose_name=_('category'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    position = models.IntegerField(
        verbose_name=_('position'),
    )

    status = models.IntegerField(
        verbose_name=_('status'),
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES.disabled,
        db_index=True,
    )

    stock_quantity = models.IntegerField(
        verbose_name=_('stock quantity'),
        default=0,
    )

    stock = models.IntegerField(
        verbose_name=_('stock'),
        choices=STOCK_CHOICES,
        default=STOCK_CHOICES.in_stock,
        db_index=True,
    )

    minimum_stock_level = models.IntegerField(
        verbose_name=_('minimum stock level'),
        default=0,
    )

    maximum_stock_level = models.IntegerField(
        verbose_name=_('maximum stock level'),
        default=0,
    )

    review_count = models.PositiveIntegerField(
        verbose_name=_('review comment count'),
        default=0,
    )

    review_count_pg = models.PositiveIntegerField(
        verbose_name=_('review comment count(PG)'),
        default=0,
    )

    naver_partner = models.BooleanField(
        verbose_name=_('naver shopping partner zone status'),
        default=False,
    )

    naver_partner_title = models.CharField(
        verbose_name=_('naver shopping partner zone product name'),
        max_length=255,
        blank=True,
    )

    naver_partner_title_pg = models.CharField(
        verbose_name=_('naver shopping partner zone product name(PG)'),
        max_length=255,
        blank=True,
    )

    naver_attribute = models.CharField(
        verbose_name=_('naver attributes'),
        max_length=499,
        blank=True,
    )

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return '{} {}'.format(self.name, self.subtitle)


class ProductList(model_utils_models.TimeStampedModel):
    name = models.CharField(
        verbose_name=_('name'),
        max_length=255,
    )

    code = models.CharField(
        verbose_name=_('code'),
        max_length=255,
    )

    products = models.ManyToManyField(Product, through='ProductListMembership')

    store = models.ForeignKey(
        'shop.Store',
        verbose_name=_('store'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('product list')
        verbose_name_plural = _('product lists')

    def __str__(self):
        return self.name


class ProductListMembership(models.Model):
    product = models.ForeignKey(
        'shop.Product',
        verbose_name=_('product'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    product_list = models.ForeignKey(
        'shop.ProductList',
        verbose_name=_('product list'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    position = models.IntegerField(
        verbose_name=_('position'),
    )

    class Meta:
        verbose_name = _('product list membership')
        verbose_name_plural = _('product list membership')


class Order(model_utils_models.SoftDeletableModel, model_utils_models.TimeStampedModel):
    PAYMENT_METHOD_CHOICES = Choices(
        (0, 'bank_transfer', _('Bank Transfer')),
        (1, 'escrow', _('Escrow (KB)')),
        (2, 'paypal', _('PayPal')),
        (3, 'credit_card', _('Credit Card')),
        (4, 'bank_transfer_pg', _('Bank Transfer (PG)')),
        (5, 'virtual_account', _('Virtual Account')),
        (6, 'phone_bill', _('Phone Bill')),
    )

    # TODO: order status != payment status
    # ?????????????????? (total refund requested)
    # ?????????????????? (partial refund requested)
    # ??????????????? (total refund)
    # ??????????????? (partial refund)
    STATUS_CHOICES = Choices(
        (0, 'payment_pending', _('payment pending')),
        (1, 'payment_completed', _('payment completed')),
        (2, 'under_review', _('under review')),
        (3, 'payment_verified', _('payment verified')),
        (4, 'shipped', _('shipped')),
        (5, 'refund_requested', _('refund requested')),
        (6, 'refund_pending', _('refund pending')),
        (7, 'refunded1', _('refunded')),  # original order
        (8, 'refunded2', _('refunded')),  # refund order
        (9, 'voided', _('voided')),
    )

    VISIBLE_CHOICES = Choices(
        (0, 'hidden', _('Hidden')),
        (1, 'visible', _('Visible')),
    )

    CURRENCY_CHOICES = Choices('KRW', 'USD')

    order_no = models.UUIDField(
        verbose_name=_('order no'),
        unique=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        db_index=True,
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
    )

    fullname = models.CharField(
        verbose_name=_('fullname'),
        max_length=64,
        blank=True,
    )

    user_agent = models.TextField(
        verbose_name=_('user-agent'),
        blank=True,
    )

    accept_language = models.TextField(
        verbose_name=_('accept-language'),
        blank=True,
    )

    ip_address = models.GenericIPAddressField(
        verbose_name=_('IP address'),
    )

    payment_method = models.IntegerField(
        verbose_name=_('payment method'),
        choices=PAYMENT_METHOD_CHOICES,
        default=PAYMENT_METHOD_CHOICES.bank_transfer,
        db_index=True,
    )

    transaction_id = models.CharField(
        verbose_name=_('transaction id'),
        max_length=64,
        blank=True,
    )

    status = models.IntegerField(
        verbose_name=_('order status'),
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES.payment_pending,
        db_index=True,
    )

    visible = models.IntegerField(
        verbose_name=_('visible status'),
        choices=VISIBLE_CHOICES,
        default=VISIBLE_CHOICES.visible,
        db_index=True,
    )

    # Max = 999,999,999.99
    total_list_price = models.DecimalField(
        verbose_name=_('total list price'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    total_selling_price = models.DecimalField(
        verbose_name=_('total price'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    currency = StatusField(
        verbose_name=_('currency'),
        choices_name='CURRENCY_CHOICES',
    )

    message = models.TextField(
        verbose_name=_('order message'),
        blank=True,
    )

    parent = models.ForeignKey(
        'self',
        verbose_name=_('parent'),
        db_index=True,
        null=True,
        on_delete=models.CASCADE,
    )

    suspicious = models.BooleanField(
        verbose_name=_('suspicious'),
        default=False,
    )

    class Meta:
        verbose_name = _('pincoin order')
        verbose_name_plural = _('pincoin orders')

    def __str__(self):
        return f'{self.user} {self.total_selling_price} {self.created}'


class OrderPayment(model_utils_models.SoftDeletableModel, model_utils_models.TimeStampedModel):
    ACCOUNT_CHOICES = Choices(
        (0, 'kb', _('KOOKMIN BANK')),
        (1, 'nh', _('NONGHYUP BANK')),
        (2, 'shinhan', _('SHINHAN BANK')),
        (3, 'woori', _('WOORI BANK')),
        (4, 'ibk', _('IBK BANK')),
        (5, 'paypal', _('PayPal')),
    )

    order = models.ForeignKey(
        'shop.Order',
        verbose_name=_('order'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    account = models.IntegerField(
        verbose_name=_('account'),
        choices=ACCOUNT_CHOICES,
        default=ACCOUNT_CHOICES.kb,
        db_index=True,
    )

    amount = models.DecimalField(
        verbose_name=_('amount'),
        max_digits=11,
        decimal_places=2,
    )

    balance = models.DecimalField(
        verbose_name=_('balance'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    received = models.DateTimeField(
        verbose_name=_('received date'),
    )

    class Meta:
        verbose_name = _('order payment')
        verbose_name_plural = _('order payments')

    def __str__(self):
        return f'order - {self.order.order_no} / payment - {self.account} {self.amount} {self.received}'


class OrderProduct(model_utils_models.SoftDeletableModel, model_utils_models.TimeStampedModel):
    order = models.ForeignKey(
        'shop.Order',
        verbose_name=_('order'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        verbose_name=_('product name'),
        max_length=255,
    )

    subtitle = models.CharField(
        verbose_name=_('product subtitle'),
        max_length=255,
        blank=True,
    )

    code = models.CharField(
        verbose_name=_('product code'),
        max_length=255,
    )

    # Max = 999,999,999.99
    list_price = models.DecimalField(
        verbose_name=_('list price'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    selling_price = models.DecimalField(
        verbose_name=_('selling price'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    quantity = models.IntegerField(
        verbose_name=_('quantity'),
        default=0,
    )

    class Meta:
        verbose_name = _('order product')
        verbose_name_plural = _('order products')

    def __str__(self):
        return f'order - {self.order.order_no} / product - {self.name}'


class OrderProductVoucher(model_utils_models.SoftDeletableModel, model_utils_models.TimeStampedModel):
    order_product = models.ForeignKey(
        'shop.OrderProduct',
        verbose_name=_('order product'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    voucher = models.ForeignKey(
        'shop.Voucher',
        verbose_name=_('voucher'),
        db_index=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    code = models.CharField(
        verbose_name=_('voucher code'),
        max_length=64,
    )

    revoked = models.BooleanField(
        verbose_name=_('revoked'),
        default=False,
    )

    remarks = models.CharField(
        verbose_name=_('voucher remarks'),
        max_length=64,
        blank=True,
    )

    class Meta:
        verbose_name = _('order voucher code')
        verbose_name_plural = _('order voucher codes')

    def __str__(self):
        return f'{self.order_product.name} ({self.code}-{self.remarks})'


class Voucher(model_utils_models.SoftDeletableModel, model_utils_models.TimeStampedModel):
    STATUS_CHOICES = Choices(
        (0, 'purchased', _('purchased')),
        (1, 'sold', _('sold')),
        (2, 'revoked', _('revoked')),
    )

    product = models.ForeignKey(
        'shop.Product',
        verbose_name=_('product'),
        db_index=True,
        on_delete=models.PROTECT,
    )

    code = models.CharField(
        verbose_name=_('voucher code'),
        max_length=64,
    )

    remarks = models.CharField(
        verbose_name=_('voucher remarks'),
        max_length=64,
        blank=True,
    )

    status = models.IntegerField(
        verbose_name=_('status'),
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES.purchased,
        db_index=True,
    )

    class Meta:
        verbose_name = _('voucher')
        verbose_name_plural = _('vouchers')

        unique_together = ('product', 'code',)

        indexes = [
            models.Index(fields=['code', ]),
        ]

    def __str__(self):
        return self.code


class NoticeMessage(model_utils_models.SoftDeletableModel, common_models.AbstractPage):
    CATEGORY_CHOICES = Choices(
        (0, 'common', _('Common')),
        (1, 'event', _('Game Event')),
        (2, 'price', _('Price Policy')),
    )

    store = models.ForeignKey(
        'shop.Store',
        verbose_name=_('store'),
        on_delete=models.CASCADE,
    )

    content = models.TextField(
        verbose_name=_('content'),
    )

    category = models.IntegerField(
        verbose_name=_('category'),
        choices=CATEGORY_CHOICES,
        default=CATEGORY_CHOICES.common,
        db_index=True,
    )

    class Meta:
        verbose_name = _('notice')
        verbose_name_plural = _('notice')

    def __str__(self):
        return self.title


class FaqMessage(model_utils_models.SoftDeletableModel, common_models.AbstractPage):
    CATEGORY_CHOICES = Choices(
        (0, 'registration', _('Registration')),
        (1, 'verification', _('Verification')),
        (2, 'order', _('Order/Stock')),
        (3, 'payment', _('Payment')),
        (4, 'delivery', _('Delivery')),
    )

    store = models.ForeignKey(
        'shop.Store',
        verbose_name=_('store'),
        on_delete=models.CASCADE,
    )

    content = models.TextField(
        verbose_name=_('content'),
    )

    category = models.IntegerField(
        verbose_name=_('category'),
        choices=CATEGORY_CHOICES,
        default=CATEGORY_CHOICES.registration,
        db_index=True,
    )

    position = models.IntegerField(
        verbose_name=_('position'),
    )

    class Meta:
        verbose_name = _('frequently asked question')
        verbose_name_plural = _('frequently asked questions')

    def __str__(self):
        return self.title


class CustomerQuestion(model_utils_models.SoftDeletableModel, common_models.AbstractPage):
    CATEGORY_CHOICES = Choices(
        (0, 'registration', _('Registration')),
        (1, 'verification', _('Verification')),
        (2, 'order', _('Order/Stock')),
        (3, 'payment', _('Payment')),
        (4, 'delivery', _('Late Delivery')),
    )

    store = models.ForeignKey(
        'shop.Store',
        verbose_name=_('store'),
        on_delete=models.CASCADE,
    )

    order = models.ForeignKey(
        'shop.Order',
        verbose_name=_('order'),
        db_index=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    content = models.TextField(
        verbose_name=_('content'),
    )

    category = models.IntegerField(
        verbose_name=_('category'),
        choices=CATEGORY_CHOICES,
        default=CATEGORY_CHOICES.registration,
        db_index=True,
    )

    class Meta:
        verbose_name = _('customer question')
        verbose_name_plural = _('customer questions')

    def __str__(self):
        return self.title


class QuestionAnswer(model_utils_models.TimeStampedModel):
    content = models.TextField(
        verbose_name=_('content'),
    )

    question = models.ForeignKey(
        'shop.CustomerQuestion',
        verbose_name=_('question'),
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('question answer')
        verbose_name_plural = _('question answers')


class Testimonials(model_utils_models.SoftDeletableModel, common_models.AbstractPage):
    store = models.ForeignKey(
        'shop.Store',
        verbose_name=_('store'),
        on_delete=models.CASCADE,
    )

    content = models.TextField(
        verbose_name=_('content'),
    )

    class Meta:
        verbose_name = _('testimonials')
        verbose_name_plural = _('testimonials')

    def __str__(self):
        return self.title


class TestimonialsAnswer(model_utils_models.TimeStampedModel):
    content = models.TextField(
        verbose_name=_('content'),
    )

    testimonial = models.ForeignKey(
        'shop.Testimonials',
        verbose_name=_('testimonials'),
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('testimonials answer')
        verbose_name_plural = _('testimonials answers')


class ShortMessageService(model_utils_models.TimeStampedModel):
    phone_from = models.CharField(
        verbose_name=_('from phone number'),
        max_length=16,
        blank=True,
        null=True,
    )

    phone_to = models.CharField(
        verbose_name=_('to phone number'),
        max_length=16,
        blank=True,
        null=True,
    )

    content = models.TextField(
        verbose_name=_('content'),
    )

    success = models.BooleanField(
        verbose_name=_('success'),
        default=True,
    )

    class Meta:
        verbose_name = _('short message')
        verbose_name_plural = _('short messages')

    def __str__(self):
        return f'{self.phone_from} {self.phone_to} {self.created}'


class LegacyCustomer(models.Model):
    customer_id = models.IntegerField(
        verbose_name=_('customer id'),
        unique=True,
    )

    email = models.CharField(
        verbose_name=_('email'),
        max_length=254,
    )

    last_name = models.CharField(
        verbose_name=_('last name'),
        max_length=32,
    )

    first_name = models.CharField(
        verbose_name=_('first name'),
        max_length=32,
    )

    date_joined = models.DateTimeField(
        verbose_name=_('date joined'),
        blank=True,
    )

    phone = models.CharField(
        verbose_name=_('phone number'),
        max_length=16,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('legacy customer')
        verbose_name_plural = _('legacy customers')

    def __str__(self):
        return f'{self.customer_id} {self.phone}'


class LegacyOrder(models.Model):
    customer_id = models.OneToOneField(
        'shop.LegacyCustomer',
        verbose_name=_('customer id'),
        to_field='customer_id',
        db_index=True,
        on_delete=models.CASCADE,
    )

    last_purchased = models.DateTimeField(
        verbose_name=_('last purchased date'),
        blank=True,
    )

    total_order_count = models.IntegerField(
        verbose_name=_('total order count'),
        default=0,
    )

    last_total = models.DecimalField(
        verbose_name=_('last total'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    max_price = models.DecimalField(
        verbose_name=_('max price'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    average_price = models.DecimalField(
        verbose_name=_('average price'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    class Meta:
        verbose_name = _('legacy order')
        verbose_name_plural = _('legacy orders')

    def __str__(self):
        return f'{self.customer_id} {self.last_purchased} {self.total_order_count}'


class LegacyOrderProduct(models.Model):
    customer_id = models.ForeignKey(
        'shop.LegacyCustomer',
        verbose_name=_('customer id'),
        to_field='customer_id',
        db_index=True,
        on_delete=models.CASCADE,
    )

    product_name = models.CharField(
        verbose_name=_('product name'),
        max_length=128,
    )

    class Meta:
        verbose_name = _('legacy order product')
        verbose_name_plural = _('legacy order products')

    def __str__(self):
        return f'{self.customer_id} {self.product_name}'


class NaverOrder(model_utils_models.SoftDeletableModel, model_utils_models.TimeStampedModel):
    PAYMENT_METHOD_CHOICES = Choices(
        (0, 'bank_transfer', _('Bank Transfer')),
    )

    # TODO: order status != payment status
    STATUS_CHOICES = Choices(
        (0, 'payment_pending', _('payment pending')),
        (1, 'payment_completed', _('payment completed')),
        (2, 'under_review', _('under review')),
        (3, 'payment_verified', _('payment verified')),
        (4, 'shipped', _('shipped')),
        (5, 'refund_requested', _('refund requested')),
        (6, 'refund_pending', _('refund pending')),
        (7, 'refunded', _('refunded')),  # original order
        (8, 'voided', _('voided')),
    )

    order_no = models.UUIDField(
        verbose_name=_('order no'),
        unique=True,
        default=uuid.uuid4,
        editable=False
    )

    fullname = models.CharField(
        verbose_name=_('fullname'),
        max_length=64,
    )

    phone = models.CharField(
        verbose_name=_('phone number'),
        max_length=16,
    )

    payment_method = models.IntegerField(
        verbose_name=_('payment method'),
        choices=PAYMENT_METHOD_CHOICES,
        default=PAYMENT_METHOD_CHOICES.bank_transfer,
        db_index=True,
    )

    transaction_id = models.CharField(
        verbose_name=_('transaction id'),
        max_length=64,
        blank=True,
    )

    status = models.IntegerField(
        verbose_name=_('order status'),
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES.payment_verified,
        db_index=True,
    )

    # Max = 999,999,999.99
    total_list_price = models.DecimalField(
        verbose_name=_('total list price'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    total_selling_price = models.DecimalField(
        verbose_name=_('total price'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    message = models.TextField(
        verbose_name=_('order message'),
        blank=True,
    )

    class Meta:
        verbose_name = _('naver order')
        verbose_name_plural = _('naver orders')

    def __str__(self):
        return f'{self.fullname} {self.total_selling_price} {self.created}'


class NaverOrderProduct(model_utils_models.SoftDeletableModel, model_utils_models.TimeStampedModel):
    order = models.ForeignKey(
        'shop.NaverOrder',
        verbose_name=_('order'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        verbose_name=_('product name'),
        max_length=255,
    )

    subtitle = models.CharField(
        verbose_name=_('product subtitle'),
        max_length=255,
        blank=True,
    )

    code = models.CharField(
        verbose_name=_('product code'),
        max_length=255,
    )

    # Max = 999,999,999.99
    list_price = models.DecimalField(
        verbose_name=_('list price'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    selling_price = models.DecimalField(
        verbose_name=_('selling price'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    quantity = models.IntegerField(
        verbose_name=_('quantity'),
        default=0,
    )

    class Meta:
        verbose_name = _('naver order product')
        verbose_name_plural = _('naver order products')

    def __str__(self):
        return f'order - {self.order.order_no} / product - {self.name}'


class NaverOrderProductVoucher(model_utils_models.SoftDeletableModel, model_utils_models.TimeStampedModel):
    order_product = models.ForeignKey(
        'shop.NaverOrderProduct',
        verbose_name=_('order product'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    voucher = models.ForeignKey(
        'shop.Voucher',
        verbose_name=_('voucher'),
        db_index=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    code = models.CharField(
        verbose_name=_('voucher code'),
        max_length=64,
    )

    revoked = models.BooleanField(
        verbose_name=_('revoked'),
        default=False,
    )

    remarks = models.CharField(
        verbose_name=_('voucher remarks'),
        max_length=64,
        blank=True,
    )

    class Meta:
        verbose_name = _('naver order voucher code')
        verbose_name_plural = _('naver order voucher codes')

    def __str__(self):
        return f'{self.order_product.name} ({self.code}-{self.remarks})'


class NaverAdvertisementLog(model_utils_models.TimeStampedModel):
    CAMPAIGN_TYPE_CHOICES = Choices(
        (1, 'C1', '????????????'),
        (2, 'C2', '????????????'),
        (4, 'C4', '???????????????'),
    )

    MEDIA_CHOICES = Choices(
        (27758, 'M27758', '????????? ???????????? - PC'),
        (8753, 'M8753', '????????? ???????????? - ?????????'),
        (122876, 'M122876', '????????? ?????????'),
        (122875, 'M122875', '????????? ???????????? ???????????????'),
        (11068, 'M11068', '????????? ?????? - PC'),
        (33421, 'M33421', '????????? ?????? - ?????????'),
        (1525, 'M1525', '????????? ??????iN - PC'),
        (36010, 'M36010', '????????? ??????iN - ?????????'),
        (96499, 'M96499', '????????? ?????? - PC'),
        (96500, 'M96500', '????????? ?????? - ?????????'),
        (118495, 'M118495', 'ZUM - PC'),
        (118496, 'M118496', 'ZUM - ?????????'),
        (171229, 'M171229', '????????? ?????? - ?????????'),
        (171228, 'M171228', '????????? ??? - ?????????'),
        (168243, 'M168243', '????????? ??????????????? - ?????????'),
        (168242, 'M168242', '????????? ???????????? - ?????????'),
        (171227, 'M171227', '????????? ????????? - ?????????'),
        (175890, 'M175890', '????????? ?????? - ?????????'),
        (103848, 'M103848', '??????(BAND) - ?????????'),
        (38367, 'M38367', '11?????? - PC'),
        (38630, 'M38630', '11?????? - ?????????'),
        (37853, 'M37853', '2CPU'),
        (23650, 'M23650', '82cook'),
        (37420, 'M37420', 'AK??? - PC'),
        (45140, 'M45140', 'AK??? - ?????????'),
        (11069, 'M11069', 'BB'),
        (1648, 'M1648', 'G??????'),
        (131017, 'M131017', 'G?????? - ?????????'),
        (141122, 'M141122', 'SLR??????'),
        (66998, 'M66998', 'YTN'),
        (67582, 'M67582', 'YTN - ?????????'),
        (23680, 'M23680', 'iMBC'),
        (23093, 'M23093', 'it??????'),
        (81750, 'M81750', '???????????????'),
        (37588, 'M37588', '????????????'),
        (15121, 'M15121', '?????????'),
        (58824, 'M58824', '???????????? - PC'),
        (74321, 'M74321', '???????????? - ?????????'),
        (49749, 'M49749', '????????? - ?????????'),
        (41354, 'M41354', '????????????'),
        (158989, 'M158989', '???????????? - ?????????'),
        (128029, 'M128029', '?????????'),
        (23123, 'M23123', '????????? - PC'),
        (87620, 'M87620', '????????? - ?????????'),
        (168665, 'M168665', '??????????????? - PC'),
        (168666, 'M168666', '??????????????? - ?????????'),
        (14055, 'M14055', '???????????????'),
        (38329, 'M38329', '?????????'),
        (145966, 'M145966', '????????? - PC'),
        (145967, 'M145967', '????????? - ?????????'),
        (139215, 'M139215', '?????????????????? - PC'),
        (131019, 'M131019', '?????????????????? - ?????????'),
        (29978, 'M29978', '????????????'),
        (67000, 'M67000', '???????????????'),
        (141121, 'M141121', '????????????'),
        (41352, 'M41352', '???????????????'),
        (151173, 'M151173', '????????? - PC'),
        (151174, 'M151174', '????????? - ?????????'),
        (51655, 'M51655', '????????????'),
        (137282, 'M137282', '???????????? - ?????????'),
        (35324, 'M35324', '????????????'),
        (147491, 'M147491', '?????????????????? - PC'),
        (26506, 'M26506', '??????????????????'),
        (58827, 'M58827', '????????? - PC'),
        (62767, 'M62767', '????????? - ?????????'),
        (37126, 'M37126', '????????? - PC'),
        (74320, 'M74320', '????????? - ?????????'),
        (58825, 'M58825', '????????????'),
        (128030, 'M128030', '???????????????????????????'),
        (56345, 'M56345', '????????????'),
        (98128, 'M98128', '???????????? - ?????????'),
        (15124, 'M15124', '???????????? - PC'),
        (54186, 'M54186', '???????????? - ?????????'),
        (16334, 'M16334', '???????????????'),
        (84644, 'M84644', '?????????'),
        (27567, 'M27567', '?????? - PC'),
        (49745, 'M49745', '?????? - ?????????'),
        (69559, 'M69559', '????????? - ?????????'),
        (69555, 'M69555', '????????? - PC'),
        (69561, 'M69561', '????????? - ?????????'),
        (69557, 'M69557', '?????????'),
        (156872, 'M156872', '?????? - PC'),
        (156873, 'M156873', '?????? - ?????????'),
        (141763, 'M141763', '????????? - ?????????'),
        (62766, 'M62766', '????????????'),
        (51654, 'M51654', '???????????????'),
        (151175, 'M151175', '????????? - PC'),
        (20545, 'M20545', '??????????????? - PC'),
        (49748, 'M49748', '??????????????? - ?????????'),
        (18111, 'M18111', '????????????????????????'),
        (24087, 'M24087', '?????????'),
        (15119, 'M15119', '???????????? - PC'),
        (49746, 'M49746', '???????????? - ?????????'),
        (36379, 'M36379', '??????????????? - PC'),
        (45714, 'M45714', '??????????????? - ?????????'),
        (137280, 'M137280', '???????????????'),
        (137281, 'M137281', '??????????????? - ?????????'),
        (79387, 'M79387', '????????????'),
        (38193, 'M38193', '?????????'),
        (70389, 'M70389', '???????????????'),
        (1526, 'M1526', '??????'),
        (131018, 'M131018', '?????? - ?????????'),
        (131268, 'M131268', '?????????????????? - ?????????'),
        (162341, 'M162341', '????????????'),
        (49363, 'M49363', '????????????'),
        (149196, 'M149196', '????????? - ?????????'),
        (58826, 'M58826', '????????????'),
        (37131, 'M37131', '???????????? - PC'),
        (49747, 'M49747', '???????????? - ?????????'),
        (37130, 'M37130', '?????????'),
        (38197, 'M38197', '???????????? - PC'),
        (56346, 'M56346', '???????????? - ?????????'),
        (16333, 'M16333', '??????????????????'),
        (35422, 'M35422', '???????????? - PC'),
        (89270, 'M89270', '???????????? - ?????????'),
        (38628, 'M38628', '???????????????'),
        (28552, 'M28552', '???????????? - PC'),
        (51271, 'M51271', '???????????? - ?????????'),
        (29983, 'M29983', '???????????? - PC'),
        (46587, 'M46587', '???????????? - ?????????'),
        (20808, 'M20808', '?????????'),
        (38627, 'M38627', '????????????'),
        (15604, 'M15604', '????????????'),
        (29987, 'M29987', '??????A'),
        (20546, 'M20546', '??????'),
        (172112, 'M172112', '?????? - ?????????'),
        (39237, 'M39237', '????????????'),
        (19369, 'M19369', '?????????'),
        (137283, 'M137283', '????????? - ?????????'),
        (15122, 'M15122', '????????????'),
        (69558, 'M69558', '????????????'),
        (24086, 'M24086', '???????????????'),
        (20049, 'M20049', '???????????? - PC'),
        (51591, 'M51591', '???????????? - ?????????'),
        (106391, 'M106391', '??????????????? - PC'),
        (106392, 'M106392', '??????????????? - ?????????'),
        (156874, 'M156874', '???????????? - PC'),
        (49362, 'M49362', '????????????'),
        (41353, 'M41353', '???????????? - PC'),
        (69560, 'M69560', '???????????? - ?????????'),
    )

    ip_address = models.GenericIPAddressField(
        verbose_name=_('IP address'),
        db_index=True,
    )

    campaign_type = models.IntegerField(
        verbose_name=_('campaign type'),
        choices=CAMPAIGN_TYPE_CHOICES,
        default=1,
        db_index=True,
    )

    media = models.IntegerField(
        verbose_name=_('media'),
        choices=MEDIA_CHOICES,
        default=27758,
        db_index=True,
    )

    query = models.CharField(
        verbose_name=_('ad query'),
        max_length=255,
    )

    rank = models.IntegerField(
        verbose_name=_('ad rank'),
    )

    ad_group = models.CharField(
        verbose_name=_('ad group ID'),
        max_length=255,
    )

    ad = models.CharField(
        verbose_name=_('ad ID'),
        max_length=255,
    )

    keyword_id = models.CharField(
        verbose_name=_('ad keyword ID'),
        max_length=255,
    )

    keyword = models.CharField(
        verbose_name=_('ad keyword'),
        max_length=255,
    )

    user_agent = models.TextField(
        verbose_name=_('user-agent'),
        blank=True,
    )

    class Meta:
        verbose_name = _('naver advertisement log')
        verbose_name_plural = _('naver advertisement logs')

    def __str__(self):
        return f'{self.keyword}-{self.ip_address}-{self.created}'


class MileageLog(model_utils_models.SoftDeletableModel, model_utils_models.TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    order = models.ForeignKey(
        'shop.Order',
        verbose_name=_('order'),
        db_index=True,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    mileage = models.DecimalField(
        verbose_name=_('mileage'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    memo = models.TextField(
        verbose_name=_('mileage memo'),
        blank=True,
    )

    class Meta:
        verbose_name = _('mileage log')
        verbose_name_plural = _('mileage logs')

    def __str__(self):
        return f'{self.user}-{self.created}'


class PurchaseOrder(model_utils_models.SoftDeletableModel, model_utils_models.TimeStampedModel):
    title = models.CharField(
        verbose_name=_('purchase order title'),
        max_length=255,
    )

    content = models.TextField(
        verbose_name=_('purchase order content'),
    )

    paid = models.BooleanField(
        verbose_name=_('Paid'),
        default=False,
    )

    bank_account = models.CharField(
        verbose_name=_('purchase order bank account'),
        max_length=255,
        blank=True,
        null=True,
    )

    amount = models.DecimalField(
        verbose_name=_('purchase order amount'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    class Meta:
        verbose_name = _('purchase order')
        verbose_name_plural = _('purchase order')

    def __str__(self):
        return f'{self.title}-{self.created}'


class PurchaseOrderPayment(model_utils_models.SoftDeletableModel, model_utils_models.TimeStampedModel):
    ACCOUNT_CHOICES = Choices(
        (0, 'kb', _('KOOKMIN BANK')),
        (1, 'nh', _('NONGHYUP BANK')),
        (2, 'shinhan', _('SHINHAN BANK')),
        (3, 'woori', _('WOORI BANK')),
        (4, 'ibk', _('IBK BANK')),
    )

    order = models.ForeignKey(
        'shop.PurchaseOrder',
        verbose_name=_('order'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    account = models.IntegerField(
        verbose_name=_('account'),
        choices=ACCOUNT_CHOICES,
        default=ACCOUNT_CHOICES.kb,
        db_index=True,
    )

    amount = models.DecimalField(
        verbose_name=_('amount'),
        max_digits=11,
        decimal_places=2,
    )

    class Meta:
        verbose_name = _('purchase order payment')
        verbose_name_plural = _('purchase order payments')

    def __str__(self):
        return f'order - {self.order.title} / payment - {self.account} {self.amount} {self.created}'
