from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Paper(models.Model):
    PAPER_TYPES = [
        ('coated', 'coated'),
        ('uncoated', 'uncoated')
    ]

    size = models.CharField(max_length=5)
    grammage = models.CharField(max_length=5)
    paper_type = models.CharField(max_length=100, 
                                  choices=PAPER_TYPES,
                                  default='uncoated')
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Printing(models.Model):
    PRINT_TYPES = [
        ('full', 'full'),
        ('not_full', 'not full')
    ]
    LAMINATE_TYPES = [
        ('glossy', 'glossy'),
        ('matte', 'matte')
    ]

    colors_num = models.SmallIntegerField(default=4, 
                                     validators=[MaxValueValidator(4),
                                                 MinValueValidator(1)])
    overprint = models.CharField(choices=PRINT_TYPES, 
                                 default='not_full',
                                 max_length=50)
    laminate = models.CharField(max_length=50,
                                choices=LAMINATE_TYPES,
                                default='glossy')

class Dimensions(models.Model):
    height = models.SmallIntegerField(validators=[MaxValueValidator(100),
                                                 MinValueValidator(5)])
    width = models.SmallIntegerField(validators=[MaxValueValidator(100),
                                                 MinValueValidator(5)])
    depth = models.SmallIntegerField(validators=[MaxValueValidator(50),
                                                 MinValueValidator(2)])
    
    def __str__(self):
        return '{}x{}x{}'.format(self.width, self.height, self.depth)


class Bag(models.Model):
    HANDLE_TYPES = [
        ('string', 'string'),
        ('cutout', 'cutout')
    ]

    paper = models.ForeignKey('Paper', on_delete=models.CASCADE)
    printing = models.ForeignKey('Printing', on_delete=models.CASCADE)
    handle_type = models.CharField(max_length=50,
                                   choices=HANDLE_TYPES,
                                   default='string')
    dimensions = models.ForeignKey('Dimensions', on_delete=models.CASCADE)