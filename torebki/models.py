from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.


def get_price(self):
    price = PricesHistory.objects.get(
        component_type=type(self).__name__, component_id=self.id, price_to__isnull=True)
    return price.price


class Paper(models.Model):
    PAPER_TYPES = [
        ('powlekany', 'powlekany'),
        ('niepowlekany', 'niepowlekany')
    ]
    SIZE_TYPES = [
        ('A0', 'A0'),
        ('A1', 'A1'),
        ('B1', 'B1'),
        ('B2', 'B2'),
    ]
    GRAMMAGE_TYPES = [
        ('100', '100'),
        ('150', '150'),
        ('200', '200'),
    ]

    size = models.CharField(max_length=5, choices=SIZE_TYPES,
                            default='A1', verbose_name=_('size'))
    grammage = models.CharField(
        max_length=5, choices=GRAMMAGE_TYPES, default='150', verbose_name=_('grammage'))
    paper_type = models.CharField(
        max_length=100, choices=PAPER_TYPES, default='niepowlekany', verbose_name=_('paper type'))
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_('price'))
    available = models.BooleanField(default=True, verbose_name=_('available'))

    get_price = get_price

    def __str__(self):
        return f'{self.size} {dict(self.PAPER_TYPES).get(self.paper_type)}, gramatura: {self.grammage}'

    class Meta:
        verbose_name = _('paper')
        verbose_name_plural = _('papers')


class Overprint(models.Model):
    overprint_type = models.CharField(
        max_length=50, unique=True, verbose_name=_('overprint type'))
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_('price'))
    available = models.BooleanField(default=True, verbose_name=_('available'))

    get_price = get_price

    def __str__(self):
        return f'{self.overprint_type}'

    class Meta:
        verbose_name = _('overprint')
        verbose_name_plural = _('overprints')


class Laminate(models.Model):
    laminate_type = models.CharField(
        max_length=50, unique=True, verbose_name=_('laminate type'))
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_('price'))
    available = models.BooleanField(default=True, verbose_name=_('available'))

    get_price = get_price

    def __str__(self):
        return f'{self.laminate_type}'

    class Meta:
        verbose_name = _('laminate')
        verbose_name_plural = _('laminates')


class Colors(models.Model):
    colors_num = models.SmallIntegerField(default=4,
                                          validators=[MaxValueValidator(4),
                                                      MinValueValidator(1)],
                                          unique=True, verbose_name=_('number of colors'))
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_('price'))
    available = models.BooleanField(default=True, verbose_name=_('available'))

    get_price = get_price

    def __str__(self):
        return f'CMYK: {self.colors_num}'

    class Meta:
        verbose_name = _('color')
        verbose_name_plural = _('colors')


class BagDimensions(models.Model):
    height = models.SmallIntegerField(validators=[MaxValueValidator(100),
                                                  MinValueValidator(5)], verbose_name=_('height'))
    width = models.SmallIntegerField(validators=[MaxValueValidator(100),
                                                 MinValueValidator(5)], verbose_name=_('width'))
    depth = models.SmallIntegerField(validators=[MaxValueValidator(50),
                                                 MinValueValidator(2)], verbose_name=_('depth'))
    available = models.BooleanField(default=True, verbose_name=_('available'))

    def __str__(self):
        return f'{self.width}x{self.height}x{self.depth} cm'

    class Meta:
        verbose_name = _('bag dimensions')
        verbose_name_plural = _('bag dimensions')


class HandleType(models.Model):
    handle_type = models.CharField(
        max_length=50, verbose_name=_('handle type'))
    price = price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_('price'))
    available = models.BooleanField(default=True, verbose_name=_('available'))

    get_price = get_price

    def __str__(self):
        return f'{self.handle_type}'

    class Meta:
        verbose_name = _('handle type')
        verbose_name_plural = _('handle types')


class Bag(models.Model):
    paper = models.ForeignKey(
        'Paper', on_delete=models.CASCADE, verbose_name=_('paper'))

    colors_num = models.ForeignKey(
        'Colors', on_delete=models.CASCADE, verbose_name=_('number of colors'))
    overprint = models.ForeignKey(
        'Overprint', on_delete=models.CASCADE, verbose_name=_('overprint'))
    laminate = models.ForeignKey(
        'Laminate', on_delete=models.CASCADE, verbose_name=_('laminate'))

    handle_type = models.ForeignKey(
        'HandleType', on_delete=models.CASCADE, verbose_name=_('handle type'))
    dimensions = models.ForeignKey(
        'BagDimensions', on_delete=models.CASCADE, verbose_name=_('dimensions'))

    def get_price(self):
        return (
            self.paper.get_price()
            + self.colors_num.get_price()
            + self.overprint.get_price()
            + self.laminate.get_price()
            + self.handle_type.get_price()
        )

    def is_available(self):
        for component in [self.paper, self.handle_type, self.dimensions, self.colors_num,
                          self.overprint, self.laminate]:
            if not component.available:
                return False

        return True

    class Meta:
        verbose_name = _('bag')
        verbose_name_plural = _('bags')


class PricesHistory(models.Model):
    component_type = models.CharField(max_length=100)
    component_id = models.IntegerField()
    price_from = models.DateTimeField()
    price_to = models.DateTimeField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _('prices history')
        verbose_name_plural = _('prices history')
