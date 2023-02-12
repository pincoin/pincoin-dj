from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from organization import models


class TeamAdmin(MPTTModelAdmin):
    mptt_level_indent = 20


admin.site.register(models.Team, MPTTModelAdmin)
