from django.contrib import admin
from .models import Paper, Printing, Bag, Dimensions

# Register your models here.
admin.site.register(Paper)
admin.site.register(Printing)
admin.site.register(Bag)
admin.site.register(Dimensions)
