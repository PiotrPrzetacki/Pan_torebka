from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
from .models import *
import json

# Create your views here.


def index(request):
    if request.method == 'POST':
        try:
            color = Colors.objects.get(pk=request.POST['color'])
            paper = Paper.objects.get(pk=request.POST['paper'])
            laminate = Laminate.objects.get(pk=request.POST['laminate'])
            overprint = Overprint.objects.get(pk=request.POST['overprint'])
            handle_type = HandleType.objects.get(
                pk=request.POST['handle_type'])
            if 'dimensions' in request.POST:
                dimensions = BagDimensions.objects.get(
                    pk=request.POST['dimensions'])
            else:
                dimensions, created = BagDimensions.objects.get_or_create(
                    height=request.POST['custom-height'],
                    width=request.POST['custom-width'],
                    depth=request.POST['custom-depth']
                )
        except (MultiValueDictKeyError, ObjectDoesNotExist, ValueError):
            return render(request, 'torebki/bag_create_error.html')

        Bag.objects.get_or_create(paper=paper, colors_num=color, handle_type=handle_type,
                                  overprint=overprint, laminate=laminate, dimensions=dimensions)

        return render(request, 'torebki/bag_create_success.html')
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
