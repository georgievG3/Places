from django.shortcuts import render

# Create your views here.
def listing_page_view(request):
    return render(request, 'listings/listing-page.html')
