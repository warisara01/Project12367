from django.urls import path
from .views import (
    index,
    food_form_view,
    get_order_by_id,  # <-- Add this
)

urlpatterns = [
    path('', index, name='index'),
    path('form/', food_form_view, name='form'),
    path('api/orders/<str:order_id>/', get_order_by_id, name='get_order_by_id'),  # <-- Add this
]