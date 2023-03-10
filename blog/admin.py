from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from mptt.admin import DraggableMPTTAdmin

from blog import models


class PostNullFilterSpec(SimpleListFilter):
    title = _('post')
    parameter_name = 'post'

    def lookups(self, request, model_admin):
        return (
            ('1', _('Has post'),),
            ('0', _('No post'),),
        )

    def queryset(self, request, queryset):
        kwargs = {
            '{}'.format(self.parameter_name): None,
        }
        if self.value() == '0':
            return queryset.filter(**kwargs)
        if self.value() == '1':
            return queryset.exclude(**kwargs)
        return queryset


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'chunk_size', 'block_size')
    ordering = ['-created']


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'blog', 'slug', 'owner', 'category', 'published', 'status', 'is_removed', 'ip_address')
    list_filter = ('status', 'published')
    list_select_related = ('blog', 'category', 'owner')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published'
    ordering = ['status', '-published']
    raw_id_fields = ('owner',)
    readonly_fields = ('ip_address', 'view_count')


class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'slug', 'blog')
    list_filter = ('blog__title', 'created')
    prepopulated_fields = {'slug': ('title',)}
    mptt_level_indent = 20
    ordering = ['tree_id', 'lft']


class TaggedItemInline(admin.StackedInline):
    model = models.TaggedPost


class PostTagAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    list_display = ['name', 'slug']
    ordering = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'file', 'created')
    list_filter = (PostNullFilterSpec,)
    ordering = ['-created', ]


admin.site.register(models.Blog, BlogAdmin)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.PostTag, PostTagAdmin)
admin.site.register(models.Attachment, AttachmentAdmin)
