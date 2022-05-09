from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime
from .models import *


@receiver(post_save, sender=Paper)
@receiver(post_save, sender=Overprint)
@receiver(post_save, sender=Colors)
@receiver(post_save, sender=HandleType)
@receiver(post_save, sender=Laminate)
def update_price_history(sender, instance, created, **kwargs):

    def add_new_historical_price():
        historical_price = PricesHistory()
        historical_price.component_type = sender.__name__
        historical_price.component_id = instance.id
        historical_price.price = instance.price
        historical_price.save()

    if created:
        add_new_historical_price()
    else:
        last_price = PricesHistory.objects.get(component_type=sender.__name__,
                                               component_id=instance.id,
                                               price_to__isnull=True)
        if last_price.price != instance.price:
            last_price.price_to = datetime.now()
            last_price.save()
            add_new_historical_price()
