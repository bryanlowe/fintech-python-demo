from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .models import BrandShare, SalesGrowth, Industry, ProductTrends, Pricing

dataset = "test_sample"

def index(request):
    context = {}
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render(context, request))

@csrf_exempt
def brand_share(request):
    # get model data
    model = BrandShare(dataset, request.POST)
    result = model.get_data()

    # create view table
    data = model.create_database_table({}, result)
    return JsonResponse(data)

@csrf_exempt
def sales_growth(request):
    model = SalesGrowth(dataset, request.POST)
    result = model.get_data()

    # create view table
    data = model.create_database_table({}, result)
    return JsonResponse(data)

@csrf_exempt
def industry(request):
    model = Industry(dataset, request.POST)
    result = model.get_data()

    # create view table
    data = model.create_database_table({}, result)
    return JsonResponse(data)

@csrf_exempt
def product_trends(request):
    model = ProductTrends(dataset, request.POST)
    result = model.get_data()

    # create view table
    data = model.create_database_table({}, result)
    return JsonResponse(data)

@csrf_exempt
def pricing(request):
    model = Pricing(dataset, request.POST)
    result = model.get_data()

    # create view table
    data = model.create_database_table({}, result)
    return JsonResponse(data)