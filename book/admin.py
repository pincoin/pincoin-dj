from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from mptt.admin import (
    DraggableMPTTAdmin, MPTTModelAdmin
)

from book import models


class PageNullFilterSpec(SimpleListFilter):
    title = _('page')
    parameter_name = 'page'

    def queryset(self, request, queryset):
        kwargs = {
            '{}'.format(self.parameter_name): None,
        }
        if self.value() == '0':
            return queryset.filter(**kwargs)
        if self.value() == '1':
            return queryset.exclude(**kwargs)
        return queryset


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'owner', 'status', 'view_count')
    ordering = ['-created']
    raw_id_fields = ('owner',)
    readonly_fields = ('view_count', 'updated')


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'page', 'file', 'created')
    list_filter = (PageNullFilterSpec,)
    ordering = ['-created', ]


class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    mptt_level_indent = 20
    ordering = ['tree_id', 'lft']


class PageAdmin(MPTTModelAdmin):
    list_display = ('title',)
    list_filter = ('status', 'book')
    mptt_level_indent = 20
    readonly_fields = ('ip_address', 'view_count')
    ordering = ['tree_id', 'lft']


admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Attachment, AttachmentAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Page, PageAdmin)
