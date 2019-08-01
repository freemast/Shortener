from django.urls import path
from . import views

urlpatterns = [
    path("", views.ListLink.as_view(), name="list"),
    path("user-links/", views.ListUserLink.as_view(), name="user-links"),
    path("add-link/", views.AddLink.as_view()),
    path('del-link/<int:pk>', views.DelLink, name="del-link"),
    path("update-link/<int:pk>", views.UpdateLink.as_view(), name="update-link"),
    path('link/<int:pk>', views.ShowLink.as_view(), name="show-link"),
    path('tag/<int:pk>', views.ShowTagLinks.as_view(), name="show-tag-links"),
    path('<short_url>', views.Jump, name='jump-link'),
]