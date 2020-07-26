from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from Accounts.models import Accounts
from Management.models import Tags, Products, Orders, Customer
from django.db.models import Q
from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from .forms import Orderform
from django.views.generic.base import TemplateView
from datetime import datetime
from django.views.generic import DeleteView
from django.urls import reverse_lazy


class ProductsList(ListView):
    model = Products  # if queryset provided then model is not needed
    queryset = Products.objects.order_by("Productname")
    # print(queryset)
    template_name = "ProductList.html"

    def get_context_data(self, *args, **kwargs):
        # print(self.request)
        # if self.request.is_ajax():
        #     t = self.request.GET.get("TagsAjax", "None")
        #     listi = super().get_context_data(**kwargs)
        #     listi["object_list"] = Products.objects.all().filter(Tags__tags=t)
        #     print(listi["object_list"])
        #     return listi

        l = self.request.GET.get("Q", "none")
        checkbox = self.request.GET.get("Check", "none")
        print(checkbox)
        # print(l)
        if(checkbox != "none"):
            if(checkbox == "All"):
                listi = super().get_context_data(**kwargs)
                listi["Tags"] = Tags.objects.all()
                listi["object_list"] = Products.objects.all()
                return listi
            listi = super().get_context_data(**kwargs)
            listi["Tags"] = Tags.objects.all()
            listi["object_list"] = Products.objects.all().filter(
                Tags__tags=checkbox).order_by("Productname")
            return listi
        if l == "none" and checkbox == "none":
            print('out')
            context = super().get_context_data(**kwargs)
            context["Tags"] = Tags.objects.all()
            return context

        else:
            listi = super().get_context_data(**kwargs)
            listi["object_list"] = self.model.objects.filter(
                Q(Productname__icontains=l)).order_by("Productname")
            listi["Tags"] = Tags.objects.all()
            return listi


class Details(DetailView):

    model = Products
    queryset = Products.objects.all()
    template_name = "products_detail.html"


class order(CreateView):

    form_class = Orderform
    template_name = "OrderForm.html"

    def get_initial(self):
        print("Hello")
        OrderedBy = get_object_or_404(
            Products, id=self.kwargs.get('pk'))  # will accept a querset
        print(OrderedBy)
        usern = self.request.user.UserName
        return {
            'Item': OrderedBy.Productname,
            'OrderedBy': usern
        }
    # def get(self, *args, **kwargs):
    #     l = self.kwargs.get("pk", "none")
    #     print(l)


class Createorder(TemplateView):
    template_name = "UserProds.html"

    def get(self, *args, **kwargs):
        Checkthecust = Customer.objects.get(name=self.request.user.UserName)
        if(Checkthecust.Address == None):
            messages.warning(
                self.request, "Please Fill the details to continue with order")
            return HttpResponseRedirect(reverse("MyProfile"))
        ge = get_object_or_404(Products, id=self.kwargs.get('pk'))
        prname = ge
        print(prname)
        print(self.request.user.UserName)
        print(Customer.objects.all())
        obj, created = Customer.objects.get_or_create(
            Profile=self.request.user)
        Orders.objects.create(OrderedBy=obj, Item=prname,
                              Status="UnderProcessing", dateCreated=datetime.now())
        dum = Customer.objects.filter(
            name=self.request.user.UserName).first()
        # print(dum)
        # actually Ord and also both will get latest one created
        ord = dum.orders_set.latest("dateCreated")
        also = dum.orders_set.order_by('-id')[0]
        print(ord)
        print(also)
        data = ord
        details = Customer.objects.get(name=self.request.user.UserName)
        return render(self.request, self.template_name, {"data": data, "details": details})
        # Orders.save()

    # def get_context_data(self, *args, **kwargs):
    #     cont = super().get_context_data(**kwargs)

    #     print(ord)


class Orderviews(TemplateView):
    template_name = "MyOrders.html"

    def get_context_data(self, *args, **kwargs):
        cont = super().get_context_data(**kwargs)
        cont["data"] = Customer.objects.get(
            name=self.request.user.UserName).orders_set.all()
        cont["details"] = Customer.objects.get(name=self.request.user.UserName)
        # print(cont)
        return cont


class Delete(DeleteView):
    model = Orders
    success_url = reverse_lazy('MyOrders')
    template_name = "delete.html"
