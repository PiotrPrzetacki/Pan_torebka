from django.contrib import admin
from .models import *

# Register your models here.


class BagAdmin(admin.ModelAdmin):
    list_display = ('paper', 'colors_num', 'laminate', 'overprint',
                    'handle_type', 'dimensions', 'is_available', 'price')
    list_filter = ('paper__size', 'paper__paper_type', 'paper__grammage',
                   'colors_num', 'laminate', 'overprint',
                   'handle_type', 'dimensions')
    search_fields = ('paper__size', 'paper__paper_type', 'paper__grammage')

    @admin.display(description="Is available", boolean=True)
    def is_available(self, obj):
        return obj.is_available()

    @admin.display(description="Price")
    def price(self, obj):
        return f'{obj.get_price()} zł'


class PaperAdmin(admin.ModelAdmin):
    list_filter = ('size', 'grammage', 'paper_type')
    list_display = ('size', 'grammage', 'paper_type', 'price', 'available')


class HandleTypeAdmin(admin.ModelAdmin):
    search_fields = ('handle_type',)


class BagDimensionsAdmin(admin.ModelAdmin):
    search_fields = ('height', 'width', 'depth')
    list_filter = ('height', 'width', 'depth')


class LaminateAdmin(admin.ModelAdmin):
    search_fields = ('laminate_type',)


class OverprintAdmin(admin.ModelAdmin):
    search_fields = ('overprint_type',)


admin.site.register(Paper, PaperAdmin)
admin.site.register(Bag, BagAdmin)
admin.site.register(BagDimensions, BagDimensionsAdmin)
admin.site.register(HandleType, HandleTypeAdmin)
admin.site.register(Colors)
admin.site.register(Laminate, LaminateAdmin)
admin.site.register(Overprint, OverprintAdmin)
