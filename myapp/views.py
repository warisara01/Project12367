import json
from django.shortcuts import render, redirect
from .models import FoodOrder
from django.http import JsonResponse
import traceback 

def food_form_view(request, order_id=None):
    menu_items = [
        {"name": "Mediterranean Red Shells", "price": 350, "image_url": "https://images.pexels.com/photos/31779536/pexels-photo-31779536.jpeg?auto=compress&cs=tinysrgb&w=1200"},
        {"name": "Herb Garden Ravioli", "price": 280, "image_url": "https://images.pexels.com/photos/31779532/pexels-photo-31779532.jpeg?auto=compress&cs=tinysrgb&w=1200"},
        {"name": "Sun-Kissed Caprese", "price": 360, "image_url": "https://images.pexels.com/photos/31779539/pexels-photo-31779539.jpeg?auto=compress&cs=tinysrgb&w=1200"},
        {"name": "Rustic Ham Toast", "price": 280, "image_url": "https://images.pexels.com/photos/31779540/pexels-photo-31779540.jpeg?auto=compress&cs=tinysrgb&w=1200"},
        {"name": "Golden Shrimp Cream Risotto", "price": 170, "image_url": "https://images.pexels.com/photos/31779537/pexels-photo-31779537.jpeg?auto=compress&cs=tinysrgb&w=1200"},
        {"name": "Basil Blossom Delight", "price": 220, "image_url": "https://images.pexels.com/photos/31779541/pexels-photo-31779541.jpeg?auto=compress&cs=tinysrgb&w=1200"},
        {"name": "Basil Blossom Delight", "price": 190, "image_url": "https://images.pexels.com/photos/31779546/pexels-photo-31779546.jpeg?auto=compress&cs=tinysrgb&w=1200"},
        {"name": "Basil Blossom Delight", "price": 170, "image_url": "https://images.pexels.com/photos/31779543/pexels-photo-31779543.jpeg?auto=compress&cs=tinysrgb&w=1200"},
        {"name": "Basil Blossom Delight", "price": 120, "image_url": "https://images.pexels.com/photos/27827771/pexels-photo-27827771.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"},
    ]

    existing_order = None
    if order_id:
        existing_order = FoodOrder.objects.filter(pk=order_id).first()

    if request.method == "POST":
        customer = request.POST.get("customer_name")
        order_json = request.POST.get("order_data")
        order_items = json.loads(order_json)

        if existing_order:
            existing_order.delivery_status = request.POST.get("delivery_status", "รอจัดส่ง")
            existing_order.save()
        else:
            status = request.POST.get("delivery_status", "รอจัดส่ง")
            for item in order_items:
                FoodOrder.objects.create(
                    customer_name=customer,
                    item_name=item["name"],
                    quantity=item["quantity"],
                    price=item["price"],
                    delivery_status=status
                )
        return redirect('index')

    return render(request, 'form.html', {'menu_items': menu_items, 'existing_order': existing_order})

def index(request):
    all_orders = FoodOrder.objects.all()
    return render(request, 'index.html', {'all_orders': all_orders})


def get_order_by_id(request, order_id):
    try:
        orders = FoodOrder.objects.filter(id=order_id, delivery_status='confirmed')
        if not orders.exists():
            return JsonResponse({'error': 'ไม่พบคำสั่งซื้อที่ยืนยันแล้ว'}, status=404)

        results = [{
            'order_id': o.id,
            'customer_name': o.customer_name,
            'item_name': o.item_name,
            'quantity': o.quantity,
            'price': o.price,
            'order_status': o.delivery_status,  # Renamed delivery_status to order_status
        } for o in orders]

        return JsonResponse({'orders': results})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_order_by_customer_name(request):
    customer_name = request.GET.get('customer_name')
    if not customer_name:
        return JsonResponse({'error': 'Missing customer name'}, status=400)

    try:
        print("ค้นหา customer_name =", customer_name)
        orders = FoodOrder.objects.filter(customer_name=customer_name)
        if not orders.exists():
            return JsonResponse({'orders': []})

        results = [{
            'order_id': o.id,
            'customer_name': o.customer_name,
            'item_name': o.item_name,
            'quantity': o.quantity,
            'price': o.price,
            'delivery_status': o.delivery_status or 'รอจัดส่ง',  # fallback
        } for o in orders]

        return JsonResponse({'orders': results})
    except Exception as e:
        traceback.print_exc()  # แสดง stacktrace บน console
        return JsonResponse({'error': str(e)}, status=500)