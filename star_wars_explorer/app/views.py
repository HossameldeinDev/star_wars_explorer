from django.views.generic import ListView, DetailView
import petl
from django.shortcuts import redirect

from .models import Collection
from .utils import data_path, headers, crawl, collection_analytics


# Create your views here.


class CollectionListView(ListView):
    model = Collection
    template_name = "home.html"


def get_collection(request):
    collection = crawl()
    return redirect(collection)


class CollectionDetailView(DetailView):
    model = Collection
    template_name = "collection_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = petl.fromcsv(data_path / context["object"].file_name)
        context["csv_headers"] = petl.header(data)
        context["csv_rows"] = petl.listoflists(petl.data(data))
        return context


class CollectionAnalyticsView(DetailView):
    model = Collection
    template_name = "collection_analytics.html"

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return collection_analytics(request)
        else:
            return super().get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["csv_headers"] = headers
        return context
