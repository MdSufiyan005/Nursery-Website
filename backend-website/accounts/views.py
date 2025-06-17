from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from data.models import Plant
from django.http import JsonResponse
from django.db.models import Min, Max


    
@login_required
def profile(request):
    if request.user.is_authenticated:
        return redirect('display')

def home(request):
    return render(request, 'main.html', {})

@login_required
def display(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort = request.GET.get('sort', '')

    plants = Plant.objects.all()

    real_min_price = Plant.objects.aggregate(Min('price'))['price__min'] or 0
    real_max_price = Plant.objects.aggregate(Max('price'))['price__max'] or 1000

    if query:
        plants = plants.filter(name__icontains=query)

    if category:
        plants = plants.filter(Category__iexact=category)

    if min_price:
        plants = plants.filter(price__gte=min_price)

    if max_price:
        plants = plants.filter(price__lte=max_price)
    
    if sort == 'price_low':
        plants = plants.order_by('price')
    elif sort == 'price_high':
        plants = plants.order_by('-price')

    print("Filters applied:")
    print(f"Query: {query}, Category: {category}, Min: {min_price}, Max: {max_price}")
    print("Results:", plants)

    return render(request, 'home/display.html', {
        'plants': plants,
        'query': query,
        'selected_category': category,
        'min_price': min_price,
        'max_price': max_price,
        'selected_sort': sort,
        'real_min_price': real_min_price,
        'real_max_price': real_max_price
    })

@login_required
def SpecificPlant(request,plant_id):
    plant = Plant.objects.get(id=plant_id)
    return render(request, 'home/specific_plant.html', {'plant': plant})

@login_required
def search_suggestions(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        print("AJAX called with query:", query)
        products = Plant.objects.filter(name__icontains=query)[:5] # No. of suggetions
        results = [p.name for p in products]
        print("Results:", results)

    return JsonResponse({'results': results})
