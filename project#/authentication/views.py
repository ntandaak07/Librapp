

import json
import os
from pathlib import Path
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Book
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.


# Create your views here.
def home(request):
    
     return render(request, 'index.html')

def signin(request):
     if request.user.is_authenticated:
        return redirect('home')
     else:
       if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            print("working")
            login(request,user)
            return redirect('/add_book')
       context={}
     return render(request, 'signin.html') 


     
@login_required(login_url = '/admin_login')
def add_book(request):
    if request.method == "POST":
        name = request.POST['name']
        author = request.POST['author']
        isbn = request.POST['isbn']
        category = request.POST['category']

        books = Book.objects.create(name=name, author=author, isbn=isbn, category=category)
        books.save()
        return redirect("/view_books")

    return render(request, "add_book.html")  

def start(request):
    return render(request, 'authentication/start.html')

def view_books(request):
     books = Book.objects.all()
     return render(request, "view_books.html", {'books':books})


def delete_book(request, myid):
    books = Book.objects.filter(id=myid)
    books.delete()
    return redirect("/view_books")

def student_registration(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        branch = request.POST['branch']
        classroom = request.POST['classroom']
        roll_no = request.POST['roll_no']
        image = request.FILES['image']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            passnotmatch = True
            return render(request, "student_registration.html", {'passnotmatch':passnotmatch})

        user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name, last_name=last_name)
        student = Student.objects.create(user=user, phone=phone, branch=branch, classroom=classroom,roll_no=roll_no, image=image)
        user.save()
        student.save()
        alert = True
        return render(request, "student_registration.html", {'alert':alert})
    return render(request, "student_registration.html")    

def student_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse("You are not a student!!")
            else:
                return redirect("/view_books")
        else:
            alert = True
            return render(request, "student_login.html", {'alert':alert})
    return render(request, "student_login.html")

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect("/admin")
            else:
                return HttpResponse("You are not an admin.")
        else:
            alert = True
            return render(request, "admin_login.html", {'alert':alert})
    return render(request, "admin_login.html")


def search_book(request):
    if request.method=="POST":
        searched=request.POST['searched']
        books=Book.objects.filter(name__contains=searched)
        return render(request,'search_book.html',{'searched':searched,'books':books})
    else:    
        return render(request,'search_book.html',{})


def addpdf(request):
    context={'file':FilesAdmin.objects.all}
    return render(request, 'addpdf.html', context)

def download(request,path):
    file_path=os.path.join(settings.MEDIA_ROOT,path)
    if os.path.exists(file_path):
        with open(file_path,'rb')as fh:
            response=HttpResponse(fh.read(),content_type="application/adminupload")
            response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
            return response
            
    raise Http404
     
def cart(request):
    return render(request, "cart.html")





    
def addtocart(request,pk):
    book=Book.objects.get(id=pk)
    cust=Student.objects.filter(user=request.user)
    
    for c in cust:       
        carts=Cart.objects.all()
        reqcart=''
        for cart in carts:
            if(cart.student==c):
                reqcart=cart
                break
        if(reqcart==''):
            reqcart=Cart.objects.create(
                student=c,
            )
        reqcart.books.add(book)    
    return redirect('/view_books')

def checkout(request):
    cust=Student.objects.filter(user=request.user)
    for c in cust:
        carts=Cart.objects.all()
        for cart in carts:
            if(cart.student==c):
                context={
                    'cart':cart
                }
                return render(request,'checkout.html',context)  
        else:
            return render(request,'checkout.html') 
            



    
def Logout(request):
    logout(request)
    return redirect ("/")



