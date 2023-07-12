from django.shortcuts import render,redirect
from django.views.generic import View,CreateView,FormView,TemplateView,DetailView,ListView
from.forms import RegForm,LogForm
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from store.models import Product
from .models import Cart,Order
from django.contrib import messages
from django.db.models import Sum
from django.utils.decorators import method_decorator




# Create your views here.

def signin_required(fn):
    def inner(request,*args, **kwargs):
     if request.user.is_authenticated:
         return fn(request,*args,**kwargs)
     else:
         return redirect("log")
    return inner

class LogView(FormView):
    template_name="log.html"
    form_class=LogForm
    def post(self,request):
        fdata=LogForm(data=request.POST)
        if fdata.is_valid():
            uname=fdata.cleaned_data.get("username")
            pswd=fdata.cleaned_data.get("password")
            user=authenticate(request,username=uname,password=pswd)
            if user:
                login(request,user)
                return redirect("home")
            else:
                return render(request,"log.html",{"form":fdata})
    
# class RegView(View):
#     def get(self,request):
#         form=RegForm
#         return render(request,"reg.html",{"form":form})
#     def post(self,request):
#         print("reached here")
#         fdata=RegForm(data=request.POST)
     
#         if fdata.is_valid():
#             print("daat valid")
#             fdata.save()
#             return redirect("log")
#         else:
#             return render(request,"reg.html",{"form":fdata})
        
        
class RegView(CreateView):
    template_name="reg.html"
    form_class=RegForm
    success_url=reverse_lazy("log")
        
@method_decorator(signin_required,name="dispatch")
         
class CustHome(TemplateView):
   template_name="home.html"
   

   
@method_decorator(signin_required,name="dispatch")   
class ProductView(TemplateView):
     template_name="products.html"
     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"]=Product.objects.all()
        return context
    
@method_decorator(signin_required,name="dispatch")    
class Furnituredetailview(DetailView):
    template_name="furnituredetail.html"
    model=Product
    context_object_name="product"
    pk_url_kwarg="pid"
    
@signin_required   
def addcart(request,pid):
    fns=Product.objects.get(id=pid)
    user=request.user
    Cart.objects.create(product=fns,user=user)
    messages.success(request,"Product Added to Cart!!!")
    return redirect("product")

@method_decorator(signin_required,name="dispatch")
class Cartview(ListView):
    template_name="cartview.html"
    model=Cart
    context_object_name="cartitem"
    
    def get_queryset(self):
        cart=Cart.objects.filter(user=self.request.user,status="cart")
        total=Cart.objects.filter(user=self.request.user,status="cart").aggregate(tot=Sum("product__price"))
        return {"items":cart,"total":total}
    
@signin_required   
def deletecartitem(request,id):
    cart=Cart.objects.get(id=id)
    cart.delete()
    messages.error(request,"cart item removed!!!")
    return redirect("vcart")



@method_decorator(signin_required,name="dispatch")
class Checkoutview(View):
    def get(self,request,*args, **kwargs):
        return render(request,"checkout.html")
    def post(self,request,*args, **kwargs):
        id=kwargs.get("cid")
        cart=Cart.objects.get(id=id)
        prod=cart.product
        user=request.user
        address=request.POST.get("address")
        ph=request.POST.get("phone")
        Order.objects.create(product=prod,user=user,address=address,phone=ph)
        cart.status="Order Placed"
        cart.save()
        messages.success(request,"Order Placed Successfully!!!")
        return redirect("vcart")
    
    
@method_decorator(signin_required,name="dispatch")    
class Myorder(ListView):
    template_name="myorder.html"
    model=Order
    context_object_name="myorder"
    
    def get_queryset(self):
        myorder=Order.objects.filter(user=self.request.user)
        return {"order":myorder}
    
    
@signin_required   
def cancel_order(request,id):
    order=Order.objects.get(id=id)
    order.status="Cancel"
    order.save()
    messages.success(request,"Order Cancelled!!!")
    return redirect("myorder")
    
        
        
class Logoutview(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("log")
    
@method_decorator(signin_required,name="dispatch")    
class Search(View):
    def get(self,request,*args,**kwargs):
        search=request.GET.get("search")
        product=Product.objects.filter(category__icontains=search)
        context = {"searchpro":product}
        return render(request,"search.html",context)
        