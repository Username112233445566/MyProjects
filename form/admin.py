from django.contrib import admin
from .models import Form, Result


admin.site.register(Form)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('form', 'answer')
    list_filter = ('form', 'answer')