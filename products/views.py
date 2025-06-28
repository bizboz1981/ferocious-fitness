from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Product


# Create your views here.
def product_list(request):
    category_name = request.GET.get("category")
    search_query = request.GET.get("search")
    sort_by = request.GET.get("sort_by")

    products = Product.objects.all()

    if category_name:
        products = products.filter(category__name=category_name)

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(
                description__icontains=search_query)
        )

    if sort_by == "price_asc":
        products = products.order_by("price")
    elif sort_by == "price_desc":
        products = products.order_by("-price")

    return render(request, "products/product_list.html", {"products": products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "products/product_detail.html", {"product": product})
