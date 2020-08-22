from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login-register', views.addToDatabase),
    path('wishes', views.showWishes),
    path('logOut', views.logOut),
    path('wishes/new', views.addWish),
    path('wishes/remove/<int:wish_id>', views.removeWish),
    path('addWishToDataBase', views.addWishToDataBase),
    path('wishes/edit/<int:wish_id>', views.editWish),
    path('wishes/edit/<int:wish_id>/changeDatBase', views.editWishInDataBase),
    path('wishes/grant/<int:wish_id>', views.grantWish),
    path('wishes/like/<int:wish_id>', views.likeWish),
    path('wishes/stats', views.showStats),
]