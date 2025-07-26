from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from admin_panel.forms import  BlogPostForm, BlogPostBlockFormSet
from listings.forms import AddListingForm, AddListingLocationForm, MonthlyPriceFormSet
from listings.models import Listing


# Create your views here.
class PendingListingsView(ListView):
    model = Listing
    context_object_name = 'pending_listings'
    template_name = 'admin_panel/pending_listings.html'

    def get_queryset(self):
        return Listing.objects.filter(is_approved=False)


class ReviewListingView(DetailView):
    model = Listing
    template_name = 'admin_panel/review-listing.html'
    context_object_name = 'listing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = AddListingForm(instance=self.object)
        for field in form.fields.values():
            field.disabled = True
        context['form'] = form

        location_form = AddListingLocationForm(instance=self.object.location)
        for field in location_form.fields.values():
            field.disabled = True
        context['location_form'] = location_form

        formset = MonthlyPriceFormSet(instance=self.object)
        for form in formset.forms:
            for field in form.fields.values():
                field.disabled = True
        context['monthly_price_formset_edit'] = formset

        context['images'] = self.object.images.all()

        return context


class ApproveListingView(View):

    def post(self, request, slug):
        listing = Listing.objects.get(slug=slug)
        listing.is_approved = True
        listing.save()
        return redirect('pending_listings')


def create_blog_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        formset = BlogPostBlockFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            blog_post = form.save(commit=False)
            blog_post.save()
            blocks = formset.save(commit=False)
            for block in blocks:
                block.blog_post = blog_post
                block.save()
            return redirect('index')
    else:
        form = BlogPostForm()
        formset = BlogPostBlockFormSet()

    return render(request, 'admin_panel/add-blog-post.html', {
        'form': form,
        'formset': formset
    })

