from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('', views.home ,name='authentication/index'),
   path('signin/',views.signin,name='authentication/signin'),
   path("student_registration/", views.student_registration, name = 'authentication/student_registration'),
   path("start", views.start, name= 'authentication/start'),
   path("add_book/", views.add_book, name= 'authentication/add_book'),
   path("view_books/", views.view_books, name= 'authentication/view_books'),
   path("student_login/", views.student_login, name= 'authentication/student_login'),
   path("admin_login/", views.admin_login, name= 'authentication/admin_login'),
   path("delete_book/<int:myid>/", views.delete_book, name="delete_book"),
   path("logout/", views.Logout, name="logout"),
   path('addpdf/', views.addpdf ,name='authentication/addpdf'),
   path('cart/', views.cart ,name='authentication/cart'),
   path('checkout/', views.checkout ,name='authentication/checkout'),
   path('addtocart/<str:pk>', views.addtocart,name='addtocart'),
   path('search_book/',views.search_book, name='search_book'),
]

   
  
   
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT,)