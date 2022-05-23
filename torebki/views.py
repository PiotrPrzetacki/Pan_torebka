from django.shortcuts import render
from .models import *
import json
from django.forms.models import model_to_dict

# Create your views here.


def index(request):
    colors = list(Colors.objects.all())
    papers = list(Paper.objects.all())
    overprints = list(Overprint.objects.all())
    laminates = list(Laminate.objects.all())
    handle_types = list(HandleType.objects.all())
    dimensions = list(BagDimensions.objects.all())
    fields = [papers, colors, overprints, laminates, handle_types, dimensions]
    data = {'papers': [], 'colors': [], 'overprints': [],
            'laminates': [], 'handleTypes': [], 'bagDimensions': []}

    for i, field in enumerate(fields):
        for obj in field:
            if not obj.available:
                continue
            model_dict = model_to_dict(obj)
            if 'price' in model_dict:
                model_dict['price'] = float(model_dict['price'])
            data[list(data)[i]].append(model_dict)

    data = json.dumps(data)

    return render(request, 'torebki/index.html', {'data': data})
