from django.urls import path
from . import views

urlpatterns = [
    path("emsg", views.EmsgListView.as_view(), name="notification-message--emsg-list"),
    path("emsg/<str:pk>", views.EmsgDetailView.as_view(), name="notification-message--emsg-detail"),
]
