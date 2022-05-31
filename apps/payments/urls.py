from django.urls import path, include


#local imports
from .views import (
    GroupAPIView,
    GroupDetailAPIView,
    GroupPaymentsAPIView,
    GroupPaymentsDetailAPIView,
)


urlpatterns = [
    path("", GroupAPIView.as_view(), name="group_api"),
    path("<int:pk>/", GroupDetailAPIView.as_view(), name="group_detail_api"),
    path("payments/", GroupPaymentsAPIView.as_view(), name="payments_api"),
    path("payments/<int:pk>/", GroupPaymentsDetailAPIView.as_view(), name="payments_detail_api"), 
]