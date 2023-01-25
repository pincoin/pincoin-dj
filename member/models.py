import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from model_utils import Choices
from model_utils.models import (
    TimeStampedModel, SoftDeletableModel
)


def upload_directory_path(instance, filename):
    return f"member/{now().strftime('%Y-%m-%d')}/{uuid.uuid4()}.{filename.split('.')[-1]}"


class Profile(TimeStampedModel):
    PHONE_VERIFIED_STATUS_CHOICES = Choices(
        (0, 'unverified', _('cellphone unverified')),
        (1, 'verified', _('cellphone verified')),
        (2, 'revoked', _('cellphone revoked'))
    )

    GENDER_CHOICES = Choices(
        (0, 'female', _('female')),
        (1, 'male', _('male')),
    )

    DOMESTIC_CHOICES = Choices(
        (0, 'foreign', _('foreign')),
        (1, 'domestic', _('domestic')),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    phone = models.CharField(
        verbose_name=_('phone number'),
        max_length=16,
        blank=True,
        null=True,
    )

    address = models.CharField(
        verbose_name=_('address'),
        max_length=255,
        blank=True,
    )

    phone_verified = models.BooleanField(
        verbose_name=_('phone verified'),
        default=False,
    )

    phone_verified_status = models.IntegerField(
        verbose_name=_('cellphone verified status'),
        choices=PHONE_VERIFIED_STATUS_CHOICES,
        default=PHONE_VERIFIED_STATUS_CHOICES.unverified,
        db_index=True,
    )

    document_verified = models.BooleanField(
        verbose_name=_('document verified'),
        default=False,
    )

    allow_order = models.BooleanField(
        verbose_name=_('allow order'),
        default=False,
    )

    photo_id = ThumbnailerImageField(
        verbose_name=_('photo ID'),
        upload_to=upload_directory_path,
        blank=True,
    )

    card = ThumbnailerImageField(
        verbose_name=_('bank account or debit/credit card'),
        upload_to=upload_directory_path,
        blank=True,
    )

    total_order_count = models.IntegerField(
        verbose_name=_('total order count'),
        default=0,
    )

    first_purchased = models.DateTimeField(
        verbose_name=_('first purchased date'),
        null=True,
    )

    last_purchased = models.DateTimeField(
        verbose_name=_('last purchased date'),
        null=True,
    )

    not_purchased_months = models.BooleanField(
        verbose_name=_('not purchased for months'),
        default=False,
    )

    repurchased = models.DateTimeField(
        verbose_name=_('re-purchased date'),
        null=True,
    )

    max_price = models.DecimalField(
        verbose_name=_('max price'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    total_list_price = models.DecimalField(
        verbose_name=_('total list price'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    total_selling_price = models.DecimalField(
        verbose_name=_('total selling price'),
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

    mileage = models.DecimalField(
        verbose_name=_('mileage'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    memo = models.TextField(
        verbose_name=_('user memo'),
        blank=True,
    )

    date_of_birth = models.DateField(
        verbose_name=_('date of birth'),
        blank=True,
        null=True,
    )

    gender = models.IntegerField(
        verbose_name=_('gender'),
        choices=GENDER_CHOICES,
        default=GENDER_CHOICES.male,
        db_index=True,
    )

    domestic = models.IntegerField(
        verbose_name=_('domestic'),
        choices=DOMESTIC_CHOICES,
        default=DOMESTIC_CHOICES.domestic,
        db_index=True,
    )

    telecom = models.CharField(
        verbose_name=_('telecom'),
        max_length=16,
        blank=True,
    )

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self):
        return f'{self.id} profile - user {self.user.id}/{self.user.username}'


class LoginLog(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
    )

    ip_address = models.GenericIPAddressField(
        verbose_name=_('IP address'),
    )

    class Meta:
        verbose_name = _('login log')
        verbose_name_plural = _('login logs')

    def __str__(self):
        return f'{self.user.email} {self.ip_address} {self.created}'


class PhoneVerificationLog(TimeStampedModel):
    GENDER_CHOICES = Choices(
        (0, 'female', _('female')),
        (1, 'male', _('male')),
    )

    DOMESTIC_CHOICES = Choices(
        (0, 'foreign', _('foreign')),
        (1, 'domestic', _('domestic')),
    )

    token = models.CharField(
        verbose_name=_('token'),
        max_length=255,
        blank=True,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
    )

    code = models.CharField(
        verbose_name=_('code'),
        max_length=32,
        blank=True,
    )

    reason = models.CharField(
        verbose_name=_('reason'),
        max_length=16,
        blank=True,
    )

    result_code = models.CharField(
        verbose_name=_('result code'),
        max_length=16,
        blank=True,
    )

    message = models.CharField(
        verbose_name=_('message'),
        max_length=255,
        blank=True,
    )

    transaction_id = models.CharField(
        verbose_name=_('transaction id'),
        max_length=32,
        blank=True,
    )

    di = models.CharField(
        verbose_name=_('di'),
        max_length=255,
        blank=True,
    )

    ci = models.TextField(
        verbose_name=_('ci'),
        blank=True,
    )

    fullname = models.CharField(
        verbose_name=_('fullname'),
        max_length=32,
        blank=True,
    )

    date_of_birth = models.CharField(
        verbose_name=_('date of birth'),
        max_length=16,
        blank=True,
    )

    gender = models.IntegerField(
        verbose_name=_('gender'),
        choices=GENDER_CHOICES,
        default=GENDER_CHOICES.male,
        db_index=True,
    )

    domestic = models.IntegerField(
        verbose_name=_('domestic'),
        choices=DOMESTIC_CHOICES,
        default=DOMESTIC_CHOICES.domestic,
        db_index=True,
    )

    telecom = models.CharField(
        verbose_name=_('telecom'),
        max_length=16,
        blank=True,
    )

    cellphone = models.CharField(
        verbose_name=_('cellphone'),
        max_length=32,
        blank=True,
    )

    return_message = models.CharField(
        verbose_name=_('return message'),
        max_length=255,
        blank=True,
    )

    class Meta:
        verbose_name = _('phone verification log')
        verbose_name_plural = _('phone verification logs')

    def __str__(self):
        return f'{self.fullname} {self.cellphone}'


class Mms(models.Model):
    cellphone = models.CharField(
        verbose_name=_('cellphone'),
        max_length=32,
        blank=True,
    )

    sent = models.CharField(
        verbose_name=_('sent datetime'),
        max_length=32,
        blank=True,
    )

    class Meta:
        verbose_name = _('mms')
        verbose_name_plural = _('mms')

    def __str__(self):
        return f'{self.cellphone} {self.sent}'


class MmsData(models.Model):
    MIME_CHOICES = Choices(
        (0, 'txt', _('txt')),
        (1, 'jpg', _('jpg')),
        (2, 'png', _('png')),
    )

    mime = models.IntegerField(
        verbose_name=_('mime type'),
        choices=MIME_CHOICES,
        default=MIME_CHOICES.txt,
        db_index=True,
    )

    data = models.TextField(
        verbose_name=_('data'),
    )

    mms = models.ForeignKey(
        'member.Mms',
        verbose_name=_('mms'),
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('mms data')
        verbose_name_plural = _('mms data')

    def __str__(self):
        return f'{self.cellphone} {self.sent}'


class EmailBanned(SoftDeletableModel, TimeStampedModel):
    email = models.EmailField(
        verbose_name=_('email address'),
    )

    class Meta:
        verbose_name = _('banned email address')
        verbose_name_plural = _('banned email addresses')

    def __str__(self):
        return f'{self.email} {self.created}'


class PhoneBanned(SoftDeletableModel, TimeStampedModel):
    phone = models.CharField(
        verbose_name=_('phone number'),
        max_length=16,
        default='01012341234',
    )

    class Meta:
        verbose_name = _('banned phone number')
        verbose_name_plural = _('banned phone numbers')

    def __str__(self):
        return f'{self.phone} {self.created}'
