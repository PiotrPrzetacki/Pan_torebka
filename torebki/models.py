from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

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

    size = models.CharField(max_length=5, choices=SIZE_TYPES, default='A1')
    grammage = models.CharField(
        max_length=5, choices=GRAMMAGE_TYPES, default='150')
    paper_type = models.CharField(
        max_length=100, choices=PAPER_TYPES, default='niepowlekany')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    get_price = get_price

    def __str__(self):
        return f'{self.size} {dict(self.PAPER_TYPES).get(self.paper_type)}, gramatura: {self.grammage}'


class Overprint(models.Model):
    overprint_type = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    get_price = get_price

    def __str__(self):
        return f'{self.overprint_type}'


class Laminate(models.Model):
    laminate_type = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    get_price = get_price

    def __str__(self):
        return f'{self.laminate_type}'


class Colors(models.Model):
    colors_num = models.SmallIntegerField(default=4,
                                          validators=[MaxValueValidator(4),
                                                      MinValueValidator(1)],
                                          unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    get_price = get_price

    def __str__(self):
        return f'{self.colors_num}'


class BagDimensions(models.Model):
    height = models.SmallIntegerField(validators=[MaxValueValidator(100),
                                                  MinValueValidator(5)])
    width = models.SmallIntegerField(validators=[MaxValueValidator(100),
                                                 MinValueValidator(5)])
    depth = models.SmallIntegerField(validators=[MaxValueValidator(50),
                                                 MinValueValidator(2)])
    available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.width}x{self.height}x{self.depth} cm'


class HandleType(models.Model):
    handle_type = models.CharField(max_length=50)
    price = price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    get_price = get_price

    def __str__(self):
        return f'{self.handle_type}'


class Bag(models.Model):
    paper = models.ForeignKey('Paper', on_delete=models.CASCADE)

    colors_num = models.ForeignKey('Colors', on_delete=models.CASCADE)
    overprint = models.ForeignKey('Overprint', on_delete=models.CASCADE)
    laminate = models.ForeignKey('Laminate', on_delete=models.CASCADE)

    handle_type = models.ForeignKey('HandleType', on_delete=models.CASCADE)
    dimensions = models.ForeignKey('BagDimensions', on_delete=models.CASCADE)

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


class PricesHistory(models.Model):
    component_type = models.CharField(max_length=100)
    component_id = models.IntegerField()
    price_from = models.DateTimeField()
    price_to = models.DateTimeField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
