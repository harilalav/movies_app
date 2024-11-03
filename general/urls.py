from django.urls import path

from . import views

urlpatterns = [
    path("request-count/", views.RequestCountView.as_view(), name="request_count"),
    path(
        "request-count/reset/",
        views.ResetRequestCountView.as_view(),
        name="reset_request_count",
    ),
]
