from django.urls import path

from . import views

urlpatterns = [
    path("", views.view_cart, name="view_cart"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("complete/", views.complete_order, name="complete_order"),
    path(
        "order_confirmation/<int:order_id>/",
        views.order_confirmation,
        name="order_confirmation",
    ),
]
