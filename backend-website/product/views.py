from django.shortcuts import render, redirect
from .forms import ContactMessageForm

def shop_page(request):
    return render(request, 'shop_page.html',)

# def contact_page(request):
#     return render(request, 'contact_page.html')

def contact_page(request):
    form=ContactMessageForm()
    submitted=False
    
    if request.method=="POST":
        form=ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            submitted=True
            
    return render(request, 'contact_page.html',{'form':form,'submitted':submitted})