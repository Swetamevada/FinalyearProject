from django.shortcuts import render
from SJMS.models import Users
from SJMS.models import Area
from SJMS.models import City
from SJMS.models import package
from SJMS.models import photographers
from SJMS.models import feedback
from SJMS.models import Booking
from SJMS.models import p_package
from SJMS.models import category
from SJMS.models import contactus
from SJMS.models import gallery
from SJMS.form import AreaForm
from SJMS.form import CityForm
from SJMS.form import p_packageForm
from SJMS.form import categoryForm
from SJMS.form import packageForm
from SJMS.form import UserForm
from SJMS.form import galleryForm
from django.shortcuts import render,redirect
from ksproject.functions import handle_uploaded_file

import random
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
import sys

# Create your views here.

def dashboard(request):
    u=Users.objects.all().count()
    f=feedback.objects.all().count()
    p=package.objects.all().count()
    b = Booking.objects.all().count()
    a = Booking.objects.filter(b_status=0).select_related("user_id")
    print("------",a.count())

    return render(request, 'dashboard.html', {'user':u, 'feed':f, 'pack':p, 'bks':b, 'booking': a})


def login(request):
    if request.method=="POST":
        name = request.POST['Email']
        pwd = request.POST['Password']
        val = Users.objects.filter(Email=name, password=pwd, is_admin=1).count()
        data = Users.objects.all()
        u = Users.objects.filter(Email=name, password=pwd, is_admin=1)
        for data in u:
            id = data.user_id

        if val == 1:
            request.session['username'] = name
            request.session['u_id'] = id
            return redirect('/dashboard/')
        else :
            messages.error(request, 'username or password are not correct')
            return render(request, "login.html")

    else:
         return render(request, 'login.html')

def adminprofile(request):
    if request.session.has_key('username'):
        usr = request.session['u_id']
        user = Users.objects.filter(user_id=usr)
        print("==")
        return render(request,"profileadmin.html", {'user':user})
    else:
        return render(request,"login.html")

def updateadmin(request):
    if request.session.has_key('username'):
        area = Area.objects.all()
        id = request.session['u_id']
        a = Users.objects.get(user_id=id)
        return render(request,'adminedit.html', {'user':a, 'area':area})
    else:
        return render(request, "login.html")

def editadmin(request, id):
    a = Users.objects.get(user_id=id)
    form = UserForm(request.POST, instance = a)
    if form.is_valid():
        form.save()
        return redirect("/dashboard/")
    return render(request, 'adminadit.html', {'user': a})


def viewuser(request):
    if request.session.has_key('username'):
        data=Users.objects.all()
        return render(request, 'user.html',{'users': data})
    else:
        return render(request, "login.html")


def viewarea(request):
    if request.session.has_key('username'):
        a=Area.objects.all()
        return render(request, 'area.html', {'area': a})
    else:
        return render(request, "login.html")

def viewcity(request):
    if request.session.has_key('username'):
        c=City.objects.all()
        return render(request, 'city.html', {'city': c})
    else:
        return render(request, "login.html")

def viewcontact(request):
    if request.session.has_key('username'):
        a=contactus.objects.all()
        return render(request, 'contactus.html', {'cn': a})
    else:
        return render(request, "login.html")


def areainsert(request):
    citynames = City.objects.all()
    if request.method == "POST" :
        form = AreaForm(request.POST)
        print("+++++++",form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect('/areatable')
            except:
                pass

    else:
        form = AreaForm()
    ##return render(request, "insertuser.html", {'form': form})
    return render(request, "areainsert.html", {'form': form, 'cityname': citynames})

def areadelete(request, id):
    deletdata = Area.objects.get(area_id=id)
    deletdata.delete()
    return redirect("/areatable")


def areaupdate(request, id):
    city = City.objects.all()
    a = Area.objects.get(area_id=id)
    return render(request,'areaupdate.html', {'area':a, 'city':city})

def editarea(request, id):
    a = Area.objects.get(area_id=id)
    form = AreaForm(request.POST, instance = a)
    if form.is_valid():
        form.save()
        return redirect("/areatable")
    return render(request, 'areaupdate.html', {'area': a})

def cityinsert(request):
    if request.method == "POST" :
        form = CityForm(request.POST)
        print("+++++++",form.errors)
        if form.is_valid():
            try:

                form.save()
                return redirect('/citytable')
            except:
                pass
    else:
        form = CityForm()
    return render(request, "cityinsert.html", {'form': form})


def citydelete(request, id):
    deletdata = City.objects.get(city_id=id)
    deletdata.delete()
    return redirect("/citytable")

def cityupdate(request, id):
    a = City.objects.get(city_id=id)
    return render(request,'cityupdate.html', {'city':a})


def editcity(request, id):
    a = City.objects.get(city_id=id)
    form = CityForm(request.POST, instance = a)
    if form.is_valid():
        form.save()
        return redirect("/citytable")
    return render(request, 'cityupdate.html', {'city': a})


def viewphotographer(request):
    if request.session.has_key('username'):
        a = photographers.objects.all()
        return render(request, 'photographer.html', {'photo': a})
    else:
        return render(request, "login.html")

def viewfeedback(request):
    if request.session.has_key('username'):
        a = feedback.objects.all()
        return render(request, 'feedback.html', {'fd': a})
    else:
        return render(request, "login.html")

def feedbackdelete(request, id):
    deletdata = feedback.objects.get(f_id=id)
    deletdata.delete()
    return redirect("/feedbacktable")

def viewbooking(request):
    if request.session.has_key('username'):
        a = Booking.objects.all()
        return render(request, 'Booking.html', {'booking': a})
    else:
        return render(request, "login.html")

def viewp_package(request):
    if request.session.has_key('username'):
        a = p_package.objects.all()
        return render(request, 'photographerpackage.html', {'ppk': a})
    else:
        return render(request, "login.html")

def p_packageinsert(request):
    if request.method == "POST" :
        form = p_packageForm(request.POST)
        print("+++++++",form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect('/p_packagetable')
            except:
                pass

    else:
        form = p_packageForm()
    ##return render(request, "insertuser.html", {'form': form})
    return render(request, "p_packageinsert.html", {'form': form})

def p_packagedelete(request, id):
    deletdata = p_package.objects.get(p_pk_id=id)
    deletdata.delete()
    return redirect("/p_packagetable")


def p_packageupdate(request, id):
    a = p_package.objects.get(p_pk_id=id)
    return render(request,'p_packageupdate.html', {'ppk':a})


def editp_package(request, id):
    a = p_package.objects.get(p_pk_id=id)
    form = p_packageForm(request.POST, instance = a)
    if form.is_valid():
        form.save()
        return redirect("/p_packagetable")
    return render(request, 'p_packageupdate.html', {'ppk': a})


def viewcategory(request):
    if request.session.has_key('username'):
        a = category.objects.all()
        return render(request, 'category.html', {'category': a})
    else:
        return render(request, "login.html")

def categorydelete(request, id):
    deletdata = category.objects.get(c_id=id)
    deletdata.delete()
    return redirect("/categorytable")

def categoryinsert(request):

    if request.method == "POST" :
        form = categoryForm(request.POST, request.FILES)
        print("+++++++",form.errors)
        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['image_path'])
                form.save()
                return redirect('/categorytable')
            except:
                print("------------------",sys.exc_info())
                pass
    else:
        form = categoryForm()
    return render(request, "categoryinsert.html", {'form': form})

def categoryupdate(request, id):
    a = category.objects.get(c_id=id)
    return render(request,'categoryupdate.html', {'ct':a})


def editcategory(request, id):
    a = category.objects.get(c_id=id)
    form = categoryForm(request.POST, request.FILES, instance=a)
    print("---------",form.errors)
    if form.is_valid():
        handle_uploaded_file(request.FILES['image_path'])
        form.save()
        return redirect("/categorytable")
    return render(request, 'categoryupdate.html', {'ct': a})

def viewimg(request):
    if request.session.has_key('username'):
        a = gallery.objects.all()
        return render(request, 'gallery.html', {'img': a})
    else:
        return render(request, "login.html")

def imginsert(request):
    ct = category.objects.all()
    ph = photographers.objects.all()
    if request.method == "POST" :
        form = galleryForm(request.POST, request.FILES)
        print("+++++++",form.errors)
        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['g_path'])
                form.save()
                return redirect('/imgtable')
            except:
                print("------------------",sys.exc_info())
                pass
    else:
        form = galleryForm()
    return render(request, "imginsert.html", {'form': form, 'cts':ct, 'phs':ph})

def imgupdate(request, id):
    a = gallery.objects.get(g_id=id)
    ct = category.objects.all()
    ph = photographers.objects.all()
    return render(request,'galleryupdate.html', {'imgs':a, 'cts':ct, 'phs':ph})


def editimg(request, id):
    a = gallery.objects.get(g_id=id)
    form = galleryForm(request.POST, request.FILES, instance=a)
    print("---------",form.errors)
    if form.is_valid():
        handle_uploaded_file(request.FILES['g_path'])
        form.save()
        return redirect("/imgtable")
    return render(request, 'galleryupdate.html', {'imgs': a})


def imgdelete(request, id):
    deletdata = gallery.objects.get(g_id=id)
    deletdata.delete()
    return redirect("/imgtable")


def viewpackage(request):
    if request.session.has_key('username'):
        a=package.objects.all()
        return render(request, 'package.html', {'package': a})
    else:
        return render(request, "login.html")

def packageinsert(request):
    categorys = category.objects.all()
    if request.method == "POST" :
        form = packageForm(request.POST)
        print("+++++++",form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect('/packagetable')
            except:
                pass

    else:
        form = AreaForm()
    ##return render(request, "insertuser.html", {'form': form})
    return render(request, "packageinsert.html", {'form': form, 'category': categorys})

def packagedelete(request, id):
    deletdata = package.objects.get(pk_id=id)
    deletdata.delete()
    return redirect("/packagetable")

def packageupdate(request, id):
    c = category.objects.all()
    a = package.objects.get(pk_id=id)
    return render(request,'packageupdate.html', {'pks':a, 'ct': c})


def editpackage(request, id):
    a = package.objects.get(pk_id=id)
    form = packageForm(request.POST, instance = a)
    if form.is_valid():
        form.save()
        return redirect("/packagetable")
    return render(request, 'packageupdate.html', {'pks': a})



def forgot(request):
    return render(request, "forgotpassword.html")

def sendemail(request):
    otp1 = random.randint(10000, 99999)
    e = request.POST['email']
    request.session['temail']=e
    obj = Users.objects.filter(Email=e , is_admin=1).count()

    print("----------------------",obj)
    if obj == 1:
        val = Users.objects.filter(Email=e, is_admin=1).update(otp=otp1 , otp_used=0)
        subject = 'OTP Verification'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]
        send_mail(subject, message, email_from, recipient_list)
        return render(request, 'set_password.html')
    else:
        messages.error(request,"This email id is not registered.")
        return render(request, "forgotpassword.html")

def set_password(request):
    totp = request.POST['otp']
    tpassword = request.POST['password']
    cpassword = request.POST['cpassword']

    if tpassword == cpassword :
        e = request.session['temail']
        val = Users.objects.filter(Email=e, is_admin=1,otp=totp,otp_used=0).count()

        if val == 1:
            val = Users.objects.filter(Email=e, is_admin=1).update(otp_used=1,password=tpassword)
            return render(request, "login.html")

    return render(request, "set_password.html")

def logout(request):
    try:
        del request.session['username']
        del request.session['temail']
    except:
        pass

    return render(request,"login.html")