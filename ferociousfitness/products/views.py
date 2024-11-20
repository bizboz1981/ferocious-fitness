from django.shortcuts import get_object_or_404, render

from .models import Product


# Create your views here.
def product_list(request):
    category_name = request.GET.get("category")
    if category_name:
        products = Product.objects.filter(category__name=category_name)
    else:
        products = Product.objects.all()
    return render(request, "products/product_list.html", {"products": products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "products/product_detail.html", {"product": product})
