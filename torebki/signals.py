from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from datetime import datetime
from .models import *


@receiver(post_save, sender=Paper)
@receiver(post_save, sender=Overprint)
@receiver(post_save, sender=Colors)
@receiver(post_save, sender=HandleType)
@receiver(post_save, sender=Laminate)
def update_price_history(sender, instance, created, **kwargs):

    def add_new_historical_price(time_from):
        historical_price = PricesHistory()
        historical_price.component_type = sender.__name__
        historical_price.component_id = instance.id
        historical_price.price_from = time_from
        historical_price.price = instance.price

        historical_price.save()

    if created:
        add_new_historical_price(datetime.now())
    else:
        last_price = PricesHistory.objects.get(component_type=sender.__name__,
                                               component_id=instance.id,
                                               price_to__isnull=True)
        if last_price.price != instance.price:
            now = datetime.now()
            last_price.price_to = now
            last_price.save()
            add_new_historical_price(now)


@receiver(post_delete, sender=Paper)
@receiver(post_delete, sender=Overprint)
@receiver(post_delete, sender=Colors)
@receiver(post_delete, sender=HandleType)
@receiver(post_delete, sender=Laminate)
def delete_history_price(sender, instance, **kwargs):
    PricesHistory.objects.filter(
        component_type=sender.__name__, component_id=instance.id).delete()
