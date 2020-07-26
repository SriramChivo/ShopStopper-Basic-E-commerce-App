from django.shortcuts import render
from django.urls import reverse
from Accounts.models import Accounts
from .models import Tags, Products, Orders, Customer
from django.db.models import Q
from datetime import datetime, timedelta
from .forms import Editform, AddProd
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import AllowedUsers

# Create your views here.


@login_required(login_url="/login/")
@AllowedUsers(allowedroles=["Admin"])
def Homepage(request):
    Template = "Home.html"

    # print(datetime.today().date() - timedelta(days=1))
    # print(Orders.objects.filter(Q(
    #     UpdatedTime__startswith=datetime.today().date() - timedelta(days=1))))
    # & Q(UpdatedTime__startswith=datetime.today().date()))
    OrderUnderProcess = Orders.objects.filter(
        Q(Status="UnderProcessing")).count()
    OrderDelivered = Orders.objects.filter(Q(Status="Delivered")).count()
    OrderPending = Orders.objects.filter(Q(Status="Shipped")).count()
    customers = Customer.objects.first()
    products = Products.objects.all()
    # print(products)
    cuslist = Customer.objects.all()
    prodcount = {}
    for cus in products:
        # print(cus.Productname)
        # print((cus.orders_set.filter(
        #     Q(dateCreated__startswith=datetime.today().date()))).count())
        # cus.Productname = cus.orders_set.all().count
        prodcount[cus.Productname] = cus.orders_set.all().count()
    # count the max number of products on current date
    prodcount = sorted(prodcount.items(), key=lambda x: x[1], reverse=True)
    # print(prodcount)
    # for i in prodcount:
    #     print(i[0])
    #     print(i[1])
    order = Orders.objects.all()
    obj = []
    for o in order:
        l = [o.OrderedBy.name,
             o.Item.Productname, o.Item.Price, o.id, o.Status]
        obj.append(l)
    custom = Customer.objects.all()
    print(custom)
    valuableCustomer = {}
    for i in custom:
        valuableCustomer[i.name] = i.orders_set.all().count()
        # print(i.orders_set.all())
    valuableCustomer = sorted(valuableCustomer.items(),
                              key=lambda x: x[1], reverse=True)
    print(valuableCustomer)
    # print(obj)
    # break
    # print(order)
    # print(customers)
    # print(customers.orders_set.all())
    # print(products.orders_set.all())
    Context = {"OrderUnderProcess": OrderUnderProcess,
               "OrderDelivered": OrderDelivered, 'Shipped': OrderPending, "prodcount": prodcount, "obj": obj, 'valuableCustomer': valuableCustomer}
    return render(request, Template, Context)


@login_required()  # example that loginurl is set in setting.py to avoid type everytime
def Edit(request, id=id):
    orderpage = Orders.objects.get(id=id)
    # print(orderpage)
    Edit = Editform(request.POST or None, instance=orderpage)
    # print(Edit)
    template = "EditStatus.html"
    context = {"edit": Edit}
    if request.method == "POST":
        updateStatus = request.POST.get("customer_type3", None)
        # print(updateStatus)
        # print(orderpage.Status)
        orderpage.Status = updateStatus
        # print(orderpage.Status)
        orderpage.save()
        return HttpResponseRedirect(reverse("home"))
    else:
        context = {"edit": Edit}
        print("yeah")

    # print(Edit.fields.Status)
    return render(request, template, context)


@login_required()
def AddProducts(request):
    add = AddProd(request.POST or None)
    template = "AddProduct.html"
    if add.is_valid():
        prname = request.POST.get("Productname", None)
        # print(prname)
        try:
            check = Products.objects.get(Productname=prname)
            messages.error(
                request, "Product is Already there Add some new Prduct please...")
            return HttpResponseRedirect(reverse("Add"))
        except:
            tags = request.POST.getlist("Tags", None)
            # print(tags)
            # saveit = add.save(commit=False) #if anytime use commit=false to add some other requiredfields of model Need to call again the old form obj to savem2m() for m2m fields to saved in models
            # print(saveit)
            # saveit.save() #save this obj seperately saveit is an form instance on saving this m2m fields wont save
            add.save()  # this is cont if incsse not calling commit=False on form instance
            # add.save_m2m() #Should be called on old form obj (say form obj on post)
            return HttpResponseRedirect(reverse("home"))
    else:
        print(add.errors)
        # print(add.errors.Productname)
        # print(add)
    context = {"addprod": add}
    return render(request, template, context)


def updateOrder(request, id=None):
    template = "UpdateOrder.html"
    context = {}
    order = Orders.objects.get(id=id)
    edit = Editform(request.POST or None, instance=order)
    if request.method == "POST":
        if edit.is_valid():
            edit = Editform(request.POST or None, instance=order)
            check = edit.save(commit=False)
            print(check.dateCreated)
            print(check.UpdatedTime)
            print(check.Status)
            return HttpResponse("Wait")
        else:
            if edit.is_bound:
                print("no")
            # print(edit.Status)
            # print(edit.Status)
            # print(edit.OrdedredBy)
            print(edit.errors)
            return HttpResponse("Dont")
    context = {"edit": edit, "cust": Customer.objects.all(),
               "pro": Products.objects.all()}
    return render(request, template, context)
