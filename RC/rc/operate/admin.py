from django.contrib import admin
from operate.models import ChartStat
# Register your models here.

class ChartStatAdmin(admin.ModelAdmin):
    model = ChartStat
    list_display = ['age', 'gender','store','time','amount','category','location']
    verbose_name_plural = 'ChartStat'


admin.site.register(ChartStat, ChartStatAdmin)