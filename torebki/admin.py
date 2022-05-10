from django.contrib import admin
from .models import *

# Register your models here.
class BagAdmin(admin.ModelAdmin):
    list_display = ('paper', 'printing', 'handle_type', 'dimensions', 'is_available')
    list_filter = ('paper__size', 'paper__paper_type', 'paper__grammage',
    'printing', 'handle_type', 'dimensions')
    search_fields = ('paper__size', 'paper__paper_type', 'paper__grammage')

    @admin.display(description="Is available", boolean=True)
    def is_available(self, obj):
        return obj.is_available()


class PaperAdmin(admin.ModelAdmin):
    list_filter = ('size', 'grammage', 'paper_type')
    list_display = ('size', 'grammage', 'paper_type', 'price', 'available')

admin.site.register(Paper, PaperAdmin)
admin.site.register(Printing)
admin.site.register(Bag, BagAdmin)
admin.site.register(BagDimensions)
admin.site.register(HandleType)
admin.site.register(Colors)
admin.site.register(Laminate)
admin.site.register(Overprint)
