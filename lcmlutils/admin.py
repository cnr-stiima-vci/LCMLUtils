from django.contrib import admin

from models import XSDValidator, LCCS3Class, LCCS3Legend

# Register your models here.
class XSDValidatorAdmin(admin.ModelAdmin):
    model = XSDValidator
    

class LCCS3ClassAdmin(admin.ModelAdmin):
    model = LCCS3Class


class LCCS3LegendAdmin(admin.ModelAdmin):
    model = LCCS3Legend


admin.site.register(XSDValidator, XSDValidatorAdmin)
admin.site.register(LCCS3Class, LCCS3ClassAdmin)
admin.site.register(LCCS3Legend, LCCS3LegendAdmin)
