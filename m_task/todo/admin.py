from django.contrib import admin
from django.utils.html import format_html

from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'status', 'data_criacao', 'data_conclusao')
    list_filter = ('status',)
    search_fields = ('titulo', 'descricao')
    readonly_fields = ('data_criacao', 'data_conclusao')

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'status')
        }),
        ('Datas', {
            'fields': ('data_criacao', 'data_conclusao'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request)


admin.site.register(Task, TaskAdmin)
