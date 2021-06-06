from django.views.generic import ListView, DetailView

from .models import Collection


# Create your views here.


class CollectionListView(ListView):
    model = Collection
    template_name = "home.html"
