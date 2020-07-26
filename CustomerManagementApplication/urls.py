from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
"""CustomerManagementApplication URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path
from Accounts.views import Registration, loginUser, Unauth
from Management.views import Homepage, Edit, AddProducts, updateOrder
from MainApp.views import ProductsList, Details, order, Createorder, Orderviews, Delete
from MyProfiles.views import profile, logoutview
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Registration/', Registration, name="registration"),
    path('Unauth/', Unauth, name="Unauth"),
    path('', loginUser, name="homepage"),
    path('login/', loginUser, name="login"),
    re_path(r'^edit/(?P<id>\d+)/$', Edit, name="edit"),
    re_path(r'^form/(?P<id>\d+)/$', updateOrder, name="update"),
    path('home/', Homepage, name="home"),
    path('Add/', AddProducts, name="Add"),
    path('main/', ProductsList.as_view(), name="Main"),
    path('MyOrders/', Orderviews.as_view(), name="MyOrders"),
    re_path(r'^main/(?P<pk>\d+)/$', Details.as_view(), name="Details"),
    re_path(r'^delete/(?P<pk>\d+)/$', Delete.as_view(), name="Delete"),
    re_path(r'^main/(?P<pk>\d+)/order',
            order.as_view(), name="order"),
    re_path(r'^main/(?P<pk>\d+)/createorder',
            Createorder.as_view(), name="createorder"),
    path('profile/', profile, name="MyProfile"),
    path('update/', profile, name="update"),
    path('logout/', logoutview, name="logout"),
]
if settings.DEBUG is True:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
