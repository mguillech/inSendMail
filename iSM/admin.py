from iSM.models import Consorcio, Consorcista, Documento
from django.contrib import admin

class ConsorcistaInline(admin.TabularInline):
    model = Consorcista
    extra = 1

class ConsorcioAdmin(admin.ModelAdmin):
    ordering = ['name']
    inlines = [ConsorcistaInline]

class ConsorcistaAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'consorcio')
    search_fields = ['name']
    list_filter = ['consorcio']

admin.site.register(Consorcio, ConsorcioAdmin)
admin.site.register(Consorcista, ConsorcistaAdmin)
admin.site.register(Documento)
