from django.shortcuts import render

def stock_view(request):
    return render(request, 'stock.html')
