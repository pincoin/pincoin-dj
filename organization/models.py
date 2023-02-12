from django.db import models
from model_utils.models import (
    TimeStampedModel, SoftDeletableModel
)
from django.utils.translation import gettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Team(MPTTModel, TimeStampedModel):
    title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
    )

    position = models.IntegerField(
        verbose_name=_('position'),
    )

    active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
    )

    parent = TreeForeignKey(
        'self',
        verbose_name=_('parent'),
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.CASCADE,
    )

    class MPTTMeta:
        order_insertion_by = ['position']

    class Meta:
        verbose_name = _('team')
        verbose_name_plural = _('teams')

    def __str__(self):
        return self.title
