import uuid

from django.conf import settings
from django.core.files.storage import default_storage
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from model_utils import Choices
from model_utils.models import (
    TimeStampedModel
)
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from common import models as common_models


def upload_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/book/<today>/<uuid>.<ext>
    return 'book/{}/{}.{}'.format(now().strftime('%Y-%m-%d'), uuid.uuid4(), filename.split('.')[-1])


class Book(TimeStampedModel):
    STATUS_CHOICES = Choices(
        (0, 'public', _('public')),
        (1, 'private', _('private')),
    )

    LICENSE_CHOICES = Choices(
        (0, 'BY', _('BY')),
        (1, 'BY-SA', _('BY-SA')),
        (2, 'BY-ND', _('BY-ND')),
        (3, 'BY-NC', _('BY-NC')),
        (4, 'BY-NC-SA', _('BY-NC-SA')),
        (5, 'BY-NC-ND', _('BY-NC-ND')),
    )

    title = models.CharField(
        verbose_name=_('title'),
        max_length=250,
    )

    description = models.TextField(
        verbose_name=_('description'),
        blank=True,
    )

    category = TreeForeignKey(
        'book.Category',
        verbose_name=_('category'),
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )

    thumbnail = ThumbnailerImageField(
        verbose_name=_('thumbnail'),
        upload_to=upload_directory_path,
        blank=True,
    )

    status = models.IntegerField(
        verbose_name=_('status'),
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES.public,
        db_index=True,
    )

    license = models.IntegerField(
        verbose_name=_('license'),
        choices=LICENSE_CHOICES,
        default=LICENSE_CHOICES.BY,
        db_index=True,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('owner'),
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
    )

    view_count = models.PositiveIntegerField(
        verbose_name=_('view count'),
        default=0,
    )

    updated = models.DateTimeField(
        verbose_name=_('updated date'),
        null=True,
    )

    class Meta:
        verbose_name = _('book')
        verbose_name_plural = _('books')

    def __str__(self):
        return self.title


class Attachment(common_models.AbstractAttachment):
    file = models.FileField(
        verbose_name=_('uploaded file'),
        upload_to=upload_directory_path,
        storage=default_storage,
    )

    page = models.ForeignKey(
        'book.Page',
        verbose_name=_('page'),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('attachment')
        verbose_name_plural = _('attachments')


class Category(common_models.AbstractCategory):
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.title


class Page(MPTTModel, common_models.AbstractPage):
    STATUS_CHOICES = Choices(
        (0, 'draft', _('draft')),
        (1, 'public', _('public')),
        (2, 'private', _('private')),
    )

    content = models.TextField(
        verbose_name=_('content'),
    )

    book = models.ForeignKey(
        'book.Book',
        verbose_name=_('book'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    parent = TreeForeignKey(
        'self',
        verbose_name=_('parent'),
        blank=True,
        null=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )

    status = models.IntegerField(
        verbose_name=_('status'),
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES.public,
        db_index=True,
    )

    view_count = models.PositiveIntegerField(
        verbose_name=_('view count'),
        default=0,
    )

    ip_address = models.GenericIPAddressField(
        verbose_name=_('IP address'),
    )

    updated = models.DateTimeField(
        verbose_name=_('updated date'),
        null=True,
    )

    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title


class Feedback(TimeStampedModel):
    page = models.ForeignKey(
        'book.Page',
        verbose_name=_('page'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    email = models.EmailField(
        verbose_name=_('email address'),
    )

    content = models.TextField(
        verbose_name=_('content'),
    )

    class Meta:
        verbose_name = _('feedback')
        verbose_name_plural = _('feedback')
