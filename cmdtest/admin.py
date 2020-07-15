from django.contrib import admin
from cmdtest.models import Cmdcase, Cmdcasestep
# Register your models here.


class CmdcasestepAdmin(admin.TabularInline):
    list_display = ['cmdteststep', 'cmdtestobjname', 'assertdeclare', 'assertInfo1', 'assertInfo2', 'assertInfo3','assertInfo4',
                    'cmdtestresult', 'create_time', 'id', 'Cmdcase']
    model = Cmdcasestep
    extra = 1


class CmdcaseAdmin(admin.ModelAdmin):
    list_display = ['cmdcasename', 'cmdtestresult', 'create_time', 'id']
    inlines = [CmdcasestepAdmin]


admin.site.register(Cmdcase, CmdcaseAdmin)