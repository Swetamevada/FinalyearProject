from django.shortcuts import render
from SJMS.models import Users
from SJMS.models import Area
from SJMS.models import City
from SJMS.models import package
from SJMS.models import feedback
from SJMS.models import category
from SJMS.models import gallery
from SJMS.models import Booking
from SJMS.models import photographers
from SJMS.models import p_package
from SJMS.form import bookingForm
from SJMS.form import photographerForm
from SJMS.form import UserForm
from SJMS.form import contactForm
from SJMS.form import feedbackForm
from django.shortcuts import render,redirect
from ksproject.functions import handle_uploaded_file
# Create your views here.

import random
import sys, calendar
from datetime import datetime, date
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
import sys
from PIL import Image

def grayscale(request,id):
    ph = gallery.objects.get(g_id=id)
    path = ph.g_path
    img = Image.open(path).convert('LA')
    #img.save('greyscale.png')
    img.save('E:\python\ksproject\client\static\images\gray.png')
    return render(request, "fill.html")

def filtergallery(request):
    g = gallery.objects.all()
    return render(request, "filter.html", {'g':g})

def fillgrayscale(request):
    try:
        pimg = request.FILES.get('image')
        print("===", pimg)
        img = Image.open(pimg).convert('LA')
        #img.save('greyscale.png')
        img.save('E:\python\ksproject\client\static\images\gray.png')
        return render(request, "fill.html")
    except:
        pass
        messages.error(request, "please upload Your Image.")
        return render(request,"filter.html")

def home(request):
    a = package.objects.all()[:3]
    b = feedback.objects.all()
    c = category.objects.all()[:4]
    d = gallery.objects.all()
    ph = photographers.objects.all()[:3]
    u = Users.objects.all().count()
    f = feedback.objects.all().count()
    p = package.objects.all().count()
    g = photographers.objects.all().count()
    ct = category.objects.all()

    fbs = feedback.objects.all()[:3]
    return render(request, "home.html", {'pkg' : a, 'phs':ph, 'fb' : b, 'c' : c, 'img': d, 'user': u, 'fd': f, 'pk':p, 'ph':g, 'fbs':fbs, 'ct':ct})

def contact(request):
    c = category.objects.all()
    print("contact function call ------------------------")
    if request.method == "POST" :
        print("contact function call ------------------------")

        form = contactForm(request.POST)
        print("+++++++",form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect('/client/home/')
            except:
                pass
    else:
        form = contactForm()
    return render(request, "contact.html", {'form': form, 'ct':c})

def services(request,id=0):
    if id==0:
        ph = photographers.objects.all()
    else:
        ph = photographers.objects.filter(c_id_id=id)
    c = category.objects.all()
    return render(request, "services.html", {'ph':ph, 'ct':c})

def search(request):
    sch = request.GET.get('search')
    print("==",sch)
    if (photographers.objects.filter(p_name=sch)):
        ph = photographers.objects.filter(p_name=sch)
        return render(request,"services.html",{'ph':ph})
    elif (category.objects.filter(c_name=sch)):
        ct = category.objects.get(c_name=sch)
        ph = photographers.objects.filter(c_id=ct.c_id)
        return render(request, "services.html", {'ph': ph})
    elif (Area.objects.filter(area_name=sch)):
        ct = Area.objects.get(area_name=sch)
        ph = photographers.objects.filter(area_id=ct.area_id)
        return render(request, "services.html", {'ph': ph})
    else :
        return redirect('/client/services/')

def cancelbooking(request,id):
    deletdata = Booking.objects.get(b_id=id)
    deletdata.delete()
    return redirect("/client/viewbooking/")

def userprofile(request):
    if request.session.has_key('username'):
        usr = request.session['u_id']
        user = Users.objects.filter(user_id=usr)
        return render(request,"clientprofile.html", {'user':user})
    else:
        return render(request,"clientlogin.html")

def gallerytable(request):
    return render(request, "clientgallery.html")

def gallery3(request):
    return render(request, "clientgallery3.html")

def bookingview(request):
    if request.session.has_key('username'):
        dt = date.today()
        c = category.objects.all()
        uid = request.session['u_id']
        b = Booking.objects.filter(user_id=uid)
        return render(request, "viewbooking.html", {'bk':b, 'ct':c, 'dt':dt})
    else:
        return render(request,"clientlogin.html")


def blog(request):
    return render(request, "blog.html")

def planpricing(request,id=0):
    c = category.objects.all()
    if id==0:
        a=package.objects.all()
    else:
        a=package.objects.filter(c_id=id)
    return render(request, 'planpricing.html', {'pkg' : a, 'ct':c})

def categorydetail(request,id):
    c = category.objects.filter(c_id=id)
    return render(request, 'categoryviews.html', {'ct':c})

def updateprofile(request):
    if request.session.has_key('username'):
        area = Area.objects.all()
        id = request.session['u_id']
        a = Users.objects.get(user_id=id)
        return render(request,'editprofile.html', {'user':a, 'area':area})
    else:
        return render(request,"clientlogin.html")


def editprofile(request, id):
    a = Users.objects.get(user_id=id)
    form = UserForm(request.POST, instance = a)
    if form.is_valid():
        form.save()
        return redirect("/client/home")
    return render(request, 'editprofile.html', {'user': a})

def bookingupdate(request,id):
    ub = Booking.objects.get(b_id=id)
    print("==",ub.b_date)
    phs = photographers.objects.all()
    return render(request, 'bookingedit.html', {'bks':ub})

def bookingedit(request,pid,amt,id):
    bk = Booking.objects.get(b_id=id)
    phs = photographers.objects.all()
    if request.method == "POST":
        print("----post------")
        dt = request.POST['b_date']
        desc = request.POST['b_desc']
        uid = request.session['u_id']
        amnt = int(amt)
        if str(dt) <= str(date.today()) :
            messages.error(request, 'please enter valid date.')
            return render(request, 'bookingedit.html', {'bks': bk})
        else:
            if Booking.objects.filter(b_id=id, b_date=dt, p_id=pid):
                if Booking.objects.filter(b_id=id, b_date=dt, p_id=pid, payment_status=0):
                    Booking.objects.filter(b_id=id).update(b_date=dt, b_desc=desc, b_status=0)
                    return render(request,"checkoutclient.html",{'dt': dt, 'amnt': amnt, 'pid': pid, 'desc': desc, 'phs': phs, 'bid':id})
                else:
                    Booking.objects.filter(b_id=id).update(b_date=dt,b_desc=desc,b_status=0)
                    return redirect("/client/viewbooking/")
            else:
                if Booking.objects.filter(b_id=id, p_id=pid, payment_status=0):
                    Booking.objects.filter(b_id=id).update(b_date=dt, b_desc=desc, b_status=0)
                    return render(request, "checkoutclient.html",{'dt': dt, 'amnt': amnt, 'pid': pid, 'desc': desc, 'phs': phs, 'bid': id})
                else:
                    if Booking.objects.filter(b_date=dt,p_id=pid,user_id=uid):
                        messages.error(request, 'You have already booked.')
                        return render(request, 'bookingedit.html', {'bks': bk})
                    else :
                        if Booking.objects.filter(b_date=dt,p_id=pid):
                            messages.error(request, 'photographer is not available on this date.')
                            return render(request, 'bookingedit.html', {'bks': bk})
                        else:
                            Booking.objects.filter(b_id=id).update(b_date=dt, b_desc=desc,b_status=0)
                            return redirect("/client/viewbooking/")
    else :
        return render(request, 'bookingedit.html', {'bks': bk})

def bookingupdatepkg(request,id):
    ub = Booking.objects.get(b_id=id)
    print("==",ub.b_date)
    phs = photographers.objects.all()
    return render(request, 'pkgbookingedit.html', {'bks':ub, 'phs':phs})

def bookingeditpkg(request,pkid,amt,id):
    bk = Booking.objects.get(b_id=id)
    phs = photographers.objects.all()
    if request.method == "POST":
        print("----post------")
        dt = request.POST['b_date']
        desc = request.POST['b_desc']
        uid = request.session['u_id']
        ph = request.POST['p_id']
        amnt = int(amt)

        if str(dt) <= str(date.today()):
            messages.error(request, 'please enter valid date.')
            return render(request, 'pkgbookingedit.html', {'bks': bk})
        else:
            if Booking.objects.filter(b_id=id, b_date=dt, pk_id=pkid,p_id=ph):
                if Booking.objects.filter(b_id=id, b_date=dt, pk_id=pkid, p_id=ph, payment_status=0):
                    Booking.objects.filter(b_id=id).update(b_date=dt, b_desc=desc, p_id=ph, b_status=0)
                    return render(request, "checkoutpackage.html",{'dt': dt, 'amnt': amnt, 'photo': ph, 'desc': desc, 'phs': phs,'bid': id})
                else:
                    Booking.objects.filter(b_id=id).update(b_date=dt,b_desc=desc, p_id=ph, b_status=0)
                    return redirect("/client/viewbooking/")
            else:
                if Booking.objects.filter(b_date=dt,p_id=ph,user_id=uid):
                    messages.error(request, 'You have already booked.')
                    return render(request,'pkgbookingedit.html',{'bks':bk, 'phs':phs})
                else :
                    if Booking.objects.filter(b_date=dt,p_id=ph):
                        messages.error(request, 'photographer is not available on this date.')
                        return render(request,'pkgbookingedit.html',{'bks':bk, 'phs':phs})
                    else:
                        if Booking.objects.filter(b_id=id,payment_status=0):
                            Booking.objects.filter(b_id=id).update(b_date=dt, b_desc=desc, p_id=ph, b_status=0)
                            return render(request, "checkoutpackage.html",{'dt': dt, 'amnt': amnt, 'photo': ph, 'desc': desc, 'phs': phs, 'bid': id})
                        else:
                            Booking.objects.filter(b_id=id).update(b_date=dt, b_desc=desc,p_id=ph, b_status=0)
                            return redirect("/client/viewbooking/")

    else:
        return render(request,'pkgbookingedit.html',{'bks':bk, 'phs':phs})

def viewfeedback(request,id):
    c = category.objects.all()
    fd = feedback.objects.filter(p_id=id)
    return render(request,'feedbackphoto.html',{'fds':fd, 'ct':c})


def clogin(request):
    if request.method=="POST":
        name = request.POST['Email']
        pwd = request.POST['Password']
        val = Users.objects.filter(Email=name, password=pwd, is_admin=0).count()
        data = Users.objects.all()
        u = Users.objects.filter(Email=name, password=pwd, is_admin=0)
        for data in u:
            id=data.user_id

        if val == 1:
            request.session['username'] = name
            request.session['u_id'] = id
            return redirect('/client/home/')
        else:
            messages.error(request, 'username or password are not correct')
            return render(request, "clientlogin.html")

    else:
         return render(request, 'clientlogin.html')


def registration(request):
    areas = Area.objects.all()
    if request.method == "POST" :
        form = UserForm(request.POST)
        print("+++++++",form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect('/client/home/')
            except:
                print("------------------", sys.exc_info())
                pass
    else:
        form = UserForm()
    print("----------------", areas.count())
    return render(request, "registration.html", {'form': form, 'area':areas})

def pregistration(request):
    area = Area.objects.all()
    cat = category.objects.all()
    phk = p_package.objects.all()
    city = City.objects.all()
    if request.method == "POST" :
        form = photographerForm(request.POST,  request.FILES)
        print("+++++++",form.errors)
        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['p_image'])
                amnt = request.POST['p_amt']
                form.save()
                pid = photographers.objects.latest('p_id')
                return render(request, "paymentphoto.html", {'amnt':amnt , 'pid':pid})
            except:
                print("------------------", sys.exc_info())
                pass
    else:
        form = photographerForm()
    return render(request, "photoragistration.html", {'city':city,'form': form, 'pkg':phk, 'area':area, 'cat':cat })


def forgotpass(request):
    return render(request, "clientforgotpassword.html")

def sendemail(request):
    otp1 = random.randint(10000, 99999)
    e = request.POST['email']
    request.session['temail']=e
    obj = Users.objects.filter(Email=e , is_admin=0).count()

    print("----------------------", obj)
    if obj == 1:
        val = Users.objects.filter(Email=e, is_admin=0).update(otp=otp1 , otp_used=0)
        subject = 'OTP Verification'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]
        send_mail(subject, message, email_from, recipient_list)
        return render(request, 'clientset_password.html')
    else :
        messages.error(request,"This email id is not registered.")
        return render(request, "clientforgotpassword.html")

def set_password(request):
    totp = request.POST['otp']
    tpassword = request.POST['Password']
    cpassword = request.POST['CPassword']

    if tpassword == cpassword :
        e = request.session['temail']
        val = Users.objects.filter(Email=e, is_admin=0,otp=totp,otp_used=0).count()

        if val == 1:
            val = Users.objects.filter(Email=e, is_admin=0).update(otp_used=1,password=tpassword)
            return render(request, "clientlogin.html")

    return render(request, "clientset_password.html")


def packagebooking(request,id,amt):
    if request.session.has_key('username'):
        c = category.objects.all()
        id = int(id)
        phs = photographers.objects.all()
        pkg = package.objects.all()
        try:
            if request.method == "POST":
                print("----post------")
                pk = id
                dt = request.POST['b_date']
                amnt = amt
                ph = request.POST['p_id']
                desc = request.POST['b_desc']
                uid = request.session['u_id']

                p = package.objects.get(pk_id=pk)
                photo = photographers.objects.get(p_id=ph)


                if str(dt) <= str(date.today()) :
                    messages.error(request, 'please enter valid date.')
                    return render(request, "bookingpackage.html", {'pkg': pkg, 'phs':phs, 'ct':c,'id': id, 'amt': amt})
                else :
                    if Booking.objects.filter(b_date=dt, p_id=photo.p_id):
                        if Booking.objects.filter(user_id=uid, b_date=dt, p_id=photo.p_id):
                            if Booking.objects.filter(user_id=uid, b_date=dt, pk_id=p.pk_id, payment_status=0):
                                bid = Booking.objects.get(user_id=uid, pk_id=p.pk_id, b_date=dt, payment_status=0)
                                return render(request, "checkoutpackage.html",{'dt': dt, 'amnt': amnt, 'photo': photo.p_name, 'desc': desc, 'phs': phs,'bid': bid.b_id})
                            else:
                                messages.error(request, 'You have already booked.')
                                return render(request, "bookingpackage.html",{'pkg': pkg, 'phs': phs, 'ct': c, 'id': id, 'amt': amt})
                        else:
                            messages.error(request, 'photographer is not available on this date please select another photographer.')
                            return render(request, "bookingpackage.html",{'pkg': pkg, 'phs': phs, 'ct': c, 'id': id, 'amt': amt})
                    else:
                        val = Booking.objects.filter(user_id=uid, pk_id=p.pk_id, b_date=dt).count()
                        print("====", val)
                        if val == 0:
                            c = Booking(pk_id_id=p.pk_id, b_date=dt, b_amount=amnt, p_id_id=photo.p_id, b_desc=desc, b_status=0, payment_status=0, user_id_id=uid )
                            c.save()
                            bid = Booking.objects.latest('b_id')
                            return render(request,"checkoutpackage.html", {'dt':dt, 'amnt':amnt,'photo':photo.p_name,'desc':desc, 'phs':phs, 'bid':bid.b_id, 'id':id, 'pkg':pkg})
                        else :
                            if (Booking.objects.filter(user_id=uid, pk_id=p.pk_id, b_date=dt,payment_status=0)):
                                bid = Booking.objects.get(user_id=uid, pk_id=p.pk_id, b_date=dt,payment_status=0)
                                return render(request, "checkoutpackage.html",{'dt': dt, 'amnt': amnt, 'photo': photo.p_name, 'desc': desc, 'phs': phs,'bid': bid.b_id})
                            else :
                                messages.error(request, 'you have already booked.')
                                return render(request, "bookingpackage.html", {'pkg': pkg, 'phs':phs, 'ct':c, 'id':id, 'amt': amt})
        except:
                pass
                print("---error----",sys.exc_info())
        return render(request,"bookingpackage.html", {'pkg':pkg, 'phs':phs, 'ct':c, 'id':id, 'amt':amt})
    else:
        return render(request,"clientlogin.html")

def clientbooking(request,pid,amt):
    if request.session.has_key('username'):
        pid = int(pid)
        phs = photographers.objects.all()
        if request.method == "POST":
            print("----post------")
            dt = request.POST['b_date']
            amnt = int(amt)
            desc = request.POST['b_desc']
            uid = request.session['u_id']
            photo = photographers.objects.get(p_id=pid)

            if str(dt) <= str(date.today()):
                messages.error(request, 'please enter valid date.')
                return render(request, "bookingclient.html", {'phs': phs, 'pid': pid, 'amt': amt})
            else:
                if Booking.objects.filter(b_date=dt, p_id=photo.p_id):
                    if Booking.objects.filter(user_id=uid, b_date=dt, p_id=photo.p_id):
                        if Booking.objects.filter(user_id=uid, b_date=dt, p_id=photo.p_id, payment_status=0):
                            bid = Booking.objects.get(user_id=uid, p_id=photo.p_id, b_date=dt, payment_status=0)
                            return render(request, "checkoutclient.html",{'dt': dt, 'amnt': amnt, 'pid': pid, 'desc': desc, 'phs': phs, 'bid': bid.b_id})
                        else:
                            messages.error(request, 'You have already booked.')
                            return render(request, "bookingclient.html", {'phs': phs, 'pid': pid, 'amt': amt})
                    else:
                        messages.error(request, 'photographer is not available on this date please select another photographer.')
                        return render(request, "bookingclient.html", {'phs': phs, 'pid': pid, 'amt': amt})
                else:
                    val = Booking.objects.filter(user_id=uid, p_id=photo.p_id, b_date=dt).count()
                    print("====",val)
                    if val == 0 :
                        c = Booking(pk_id_id=None, b_date=dt, b_amount=amnt, p_id_id=photo.p_id, b_desc=desc, b_status=0, payment_status=0, user_id_id=uid )
                        c.save()
                        bid = Booking.objects.latest('b_id')
                        print("---", bid)
                        return render(request,"checkoutclient.html", {'dt':dt, 'amnt':amnt, 'pid':pid, 'desc':desc, 'phs':phs, 'bid':bid.b_id})
                    else :
                        if (Booking.objects.filter(user_id=uid, p_id=photo.p_id, b_date=dt, payment_status=0)):
                            bid = Booking.objects.get(user_id=uid, p_id=photo.p_id, b_date=dt, payment_status=0)
                            return render(request, "checkoutclient.html",{'dt': dt, 'amnt': amnt, 'pid': pid, 'desc': desc, 'phs': phs, 'bid': bid.b_id})
                        else :
                            messages.error(request, 'you have already booked.')
                            return render(request, "bookingclient.html", {'phs': phs, 'pid': pid, 'amt': amt})
        else :
            return render(request, "bookingclient.html", {'phs': phs, 'pid': pid, 'amt': amt})
    else:
        return render(request,"clientlogin.html")

def cash(request,id):
    b = Booking.objects.get(b_id=id)
    b.payment_status = 1
    b.save()
    print("-----------Payment success--------")
    return redirect('/client/viewbooking/')

def success(request,id):
    b = Booking.objects.get(b_id=id)
    b.payment_status = 2
    b.save()
    print("-----------Payment success--------")
    return redirect('/client/viewbooking/')

def failure(request):
    return render(request,"failure.html")

def photosuccess(request,id):
    b = photographers.objects.get(p_id=id)
    b.pay_status = 2
    b.save()
    print("-----------Payment success--------")
    return redirect('/photographer/photologin/')

def photosgallery(request):
    g = gallery.objects.all()
    c = category.objects.all()
    ph = photographers.objects.all()
    return render(request, "clientgallery.html", {'g':g, 'ct':c, 'ph':ph})

def feedbackinsert(request,pid):
    if request.session.has_key('username'):
        if request.method == "POST":
           fdesc = request.POST['f_desc']
           fdate = date.today()
           uid = request.session['u_id']
           photo = photographers.objects.get(p_id=pid)
           try:
                form = feedback(user_id_id=uid, f_date=fdate, f_desc=fdesc, p_id_id=photo.p_id)
                form.save()
                return redirect('/client/home/')
           except:
                pass
                print("---error----", sys.exc_info())
        return redirect('/client/services/')
    else:
        return render(request,"clientlogin.html")

def clientlogout(request):
    try:
        del request.session['username']
        del request.session['temail']
    except:
        pass
        return redirect('/client/home/')
