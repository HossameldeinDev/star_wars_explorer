from django.urls import path

from .views import (
    CollectionListView,
    CollectionDetailView,
    get_collection,
)

urlpatterns = [
    path("", CollectionListView.as_view(), name="home"),
    path(
        "collection/<int:pk>/", CollectionDetailView.as_view(), name="collection_detail"
    ),
    path("collection/fetcher", get_collection),
]
