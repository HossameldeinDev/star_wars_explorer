from django.urls import path

from .views import (
    CollectionListView,
    CollectionDetailView,
    get_collection,
    CollectionAnalyticsView,
)

urlpatterns = [
    path("", CollectionListView.as_view(), name="home"),
    path(
        "collection/<int:pk>/", CollectionDetailView.as_view(), name="collection_detail"
    ),
    path("collection/fetcher", get_collection),
    path(
        "collection/<int:pk>/analytics/",
        CollectionAnalyticsView.as_view(),
        name="collection_analytics",
    ),
]
