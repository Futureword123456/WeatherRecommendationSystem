from django.contrib import admin

# Register your models here.
from region.models import Region


class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'level', 'is_municipality', 'is_province_capital','is_display', 'name', 'parent']



admin.site.register(Region, RegionAdmin)
