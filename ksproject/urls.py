"""ksproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from SJMS import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', views.dashboard),
    path('login/', views.login),
    path('updateadmin/', views.updateadmin),
    path('editadmin/<int:id>', views.editadmin),
    path('imgtable/',views.viewimg),
    path('imginsert/', views.imginsert),
    path('imgdelete/<int:id>', views.imgdelete),
    path('gallery', views.imginsert),
    path('usertable/', views.viewuser),
    path('contacttable/', views.viewcontact),
    path('areatable/', views.viewarea),
    path('areainsert/', views.areainsert),
    path('areadelete/<int:id>', views.areadelete),
    path('area', views.areainsert),
    path('areaupdate/<int:id>', views.areaupdate),
    path('editarea/<int:id>', views.editarea),
    path('citytable/', views.viewcity),
    path('cityinsert/', views.cityinsert),
    path('city', views.cityinsert),
    path('citydelete/<int:id>', views.citydelete),
    path('cityupdate/<int:id>', views.cityupdate),
    path('editcity/<int:id>', views.editcity),
    path('packagetable/', views.viewpackage),
    path('packagedelete/<int:id>', views.packagedelete),
    path('packageinsert/', views.packageinsert),
    path('package', views.packageinsert),
    path('packageupdate/<int:id>', views.packageupdate),
    path('editpackage/<int:id>', views.editpackage),

    path('photographertable/', views.viewphotographer),
    path('feedbacktable/', views.viewfeedback),
    path('feedbackdelete/<int:id>', views.feedbackdelete),
    path('bookingtable/', views.viewbooking),
    path('p_packagetable/', views.viewp_package),
    path('p_packageinsert/', views.p_packageinsert),
    path('ppackage', views.p_packageinsert),
    path('p_packagedelete/<int:id>', views.p_packagedelete),
    path('p_packageupdate/<int:id>', views.p_packageupdate),
    path('editp_package/<int:id>', views.editp_package),
    path('categorytable/', views.viewcategory),
    path('categorydelete/<int:id>', views.categorydelete),
    path('categoryinsert/', views.categoryinsert),
    path('category', views.categoryinsert),
    path('categoryupdate/<int:id>', views.categoryupdate),
    path('editcategory/<int:id>', views.editcategory),
    path('forgot/', views.forgot),
    path('sendotp/', views.sendemail),
    path('reset/', views.set_password),
    path('logout/', views.logout),
    path('imgupdate/<int:id>', views.imgupdate),
    path('editimg/<int:id>', views.editimg),
   path('adminprofile/', views.adminprofile),

    path('client/', include('client.urls')),
    path('photographer/', include('photographer.urls')),
]
