from django.shortcuts import render
from .models import ProductCategory, ProductFamily, ProductModel
# Create your views here.
def products_view(request):
    categories = ProductCategory.objects.all()
    category_code = request.GET.get('category',categories[0].type_code)
    products = ProductModel.objects.prefetch_related("chip_options").filter(product_family__category__type_code=category_code)

    context = {
        'categories': categories,
        'products': products
    }
    return render(request, 'products/index.html', context)