from django.shortcuts import render, get_object_or_404
from django.urls import reverse,reverse_lazy
from Accounts.models import Accounts
from Management.models import Tags, Products, Orders, Customer
from django.db.models import Q, Prefetch
from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from .forms import customerProfile
from django.views.generic.base import TemplateView
from datetime import datetime
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, logout


def profile(request):

    customer1 = Customer.objects.get(name=request.user.UserName)
    # or
    # return Id of customer we can use in foreignke  y field like line 41
    customer2 = request.user.pk
    # or
    # OnetoOne Field Actually request.user is itself an object(simpleLazyObject) so we are accessing child customer directly
    customer = request.user.customer
    # print(request.user.pk)
    # print(type(request.user))
    print(customer)
    # Actually i and for i in Orders.objects.all() then i.item is exactly same by the look But i will not hit db everytime we access the child(or)Column like customer.orderby.name
    # returns Order Object we can access customer model without hitting db
    i = Orders.objects.select_related("OrderedBy").first()
    # print(i.Item)
    # print(Orders.objects.all())
    # returns Order Object we can access Products model without hitting db
    i2 = Orders.objects.select_related("Item").last()
    # print(i2.OrderedBy)
    # print(type(i))
    # print(i)
    # print(i2)
    # returns CustomerObject we can get all the orders without hitting db
    p1 = Customer.objects.prefetch_related("orders_set").first()
    print(p1.orders_set.all())
    p2 = Customer.objects.prefetch_related(
        Prefetch("orders_set", Orders.objects.filter(Item__Price__range=(2000, 5000))))
    for i in p2:
        print(i.orders_set.all())
    # using prefetch method to filter even those orders instead getting all()

    # or primarykey of Customer that request.user.pk else pass 2 or 3 anynumber
    o = Orders.objects.filter(OrderedBy=customer)
    # print(Orders._meta.get_all_field_names())
    print(Orders._meta.get_fields())
    for l in o:
        print(l.Item.Price)
        print(l.Item.__class__)
        print(l.OrderedBy.Phone)
    # o1 = Orders.objects.get(OrderedBy=request.user)
    print(o)
    # print(o1)
    print(request.user)
    print(request.user.customer.Phone)
    form = customerProfile(request.POST or None, instance=customer)
    if("profile" in request.get_full_path()):
        # request.user will give name chivo request.user.pk will give primary key for chivo that 1
        CusObj = Customer.objects.get(Profile=request.user.pk)
        context = {"customer": CusObj}
        template = "MyProfile.html"
        return render(request, template, context)
    else:
        if request.method == "POST":
            form = customerProfile(request.POST or None,
                                   request.FILES or None, instance=customer)
            if form.is_valid():
                print("Came IN")
                form.save()
                return HttpResponseRedirect("/profile/")

        template = "editProfile.html"
        context = {"form": form, "customer": customer}
        return render(request, template, context)

# class profile(UpdateView):
#     form_class = customerProfile
#     template_name = "MyProfile.html"

#     def get_object(self, *args, **kwargs):
#         # If incase we are passing any id in the url to update the view the
#         # getuser=Customer.objects.get(customer__id=self.request.kwargs.get('pk' (or 'id' or 'slug') defined in url patterns))
#         return self.request.user.customer


def logoutview(request):#shouldNot Name the function names as logout otherwise it will throw an error maximum recusrsion reached
    logout(request) 
    return HttpResponseRedirect(reverse_lazy("login"))
