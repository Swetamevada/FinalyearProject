from django.shortcuts import render
from SJMS.models import photographers
from SJMS.models import Booking
from SJMS.models import Users
from SJMS.models import Area
from SJMS.models import package
from SJMS.models import feedback
from SJMS.models import category
from SJMS.models import City
from SJMS.models import contactus
from SJMS.models import gallery
from SJMS.models import p_package
from SJMS.form import galleryForm
from SJMS.form import photographerForm
from ksproject.functions import handle_uploaded_file
from django.shortcuts import render,redirect
# Create your views here.

import random
import sys
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages

def photodashboard(request):
    u = Users.objects.all().count()
    f = category.objects.all().count()
    p = package.objects.all().count()
    bk = Booking.objects.all().count()
    return render(request, 'photographerhome.html', {'user' :u, 'category' :f, 'package' :p, 'bks':bk})

def photohome(request):
    if request.session.has_key('pusername'):
        u = Users.objects.all().count()
        f = category.objects.all().count()
        p = package.objects.all().count()
        pid = request.session['ph_id']
        bk = Booking.objects.filter(p_id=pid)
        b = bk.count()
        bks = Booking.objects.filter(p_id=pid, b_status=0).select_related("user_id")
        return render(request, 'photographerhome.html', {'user' :u, 'category' :f, 'package' :p, 'bks':b, 'booking':bks})
    else:
        return render(request, "photographerlogin.html")

def photologin(request):
    if request.method=="POST":
        name = request.POST['Email']
        pwd = request.POST['Password']
        val = photographers.objects.filter(p_email=name, p_password=pwd).count()
        data = photographers.objects.all()
        u = photographers.objects.filter(p_email=name, p_password=pwd)
        for data in u:
            id = data.p_id

        if val == 1:
            request.session['pusername'] = name
            request.session['ph_id'] = id
            return redirect('/photographer/photohome/')
        else:
            messages.error(request, 'username or password are not correct')
            return render(request, "photographerlogin.html")

    else:
         return render(request, 'photographerlogin.html')

def photosbooking(request):
    if request.session.has_key('pusername'):
        pid = request.session['ph_id']
        b = Booking.objects.filter(p_id=pid)
        return render(request, "photobooking.html", {'bks':b})
    else:
        return render(request, "photographerlogin.html")

def profilephoto(request):
    if request.session.has_key('pusername'):
        usr = request.session['ph_id']
        user = photographers.objects.filter(p_id=usr)
        return render(request,"photoprofile.html", {'user':user})
    else:
        return render(request,"photographerlogin.html")

def acceptbooking(request,id):
    b = Booking.objects.get(b_id=id)
    b.b_status = 1
    b.save()
    return redirect("/photographer/photohome")

def rejectbooking(request,id):
    b = Booking.objects.get(b_id=id)
    b.b_status = 2
    b.save()
    return redirect("/photographer/photohome")


def photoviewuser(request):
    if request.session.has_key('pusername'):
        data=Users.objects.all()
        return render(request, 'photouser.html',{'users': data})
    else:
        return render(request, "photographerlogin.html")

def photoviewarea(request):
    if request.session.has_key('pusername'):
        a=Area.objects.all()
        return render(request, 'photoarea.html', {'area': a})
    else:
        return render(request, "photographerlogin.html")

def photoviewcity(request):
    if request.session.has_key('pusername'):
        c=City.objects.all()
        return render(request, 'photocity.html', {'city': c})
    else:
        return render(request, "photographerlogin.html")

def photoviewcontact(request):
    if request.session.has_key('pusername'):
        a=contactus.objects.all()
        return render(request, 'photocontact.html', {'cn': a})
    else:
        return render(request, "photographerlogin.html")


def photoviewphotographer(request):
    if request.session.has_key('pusername'):
        a = photographers.objects.all()
        return render(request, 'photophotographer.html', {'photo': a})
    else:
        return render(request, "photographerlogin.html")

def photoviewfeedback(request):
    if request.session.has_key('pusername'):
        a = feedback.objects.all()
        return render(request, 'photofeedback.html', {'fd': a})
    else:
        return render(request, "photographerlogin.html")

def photoviewp_package(request):
    if request.session.has_key('pusername'):
        a = p_package.objects.all()
        return render(request, 'photophotographerpackage.html', {'ppk': a})
    else:
        return render(request, "photographerlogin.html")

def photoviewcategory(request):
    if request.session.has_key('pusername'):
        a = category.objects.all()
        return render(request, 'photocategory.html', {'category': a})
    else:
        return render(request, "photographerlogin.html")

def photoviewimg(request):
    if request.session.has_key('pusername'):
        a = gallery.objects.all()
        return render(request, 'photogallery.html', {'img': a})
    else:
        return render(request, "photographerlogin.html")

def photoviewpackage(request):
    if request.session.has_key('pusername'):
        a=package.objects.all()
        return render(request, 'photopackage.html', {'package': a})
    else:
        return render(request, "photographerlogin.html")


def photosimginsert(request):
    ct = category.objects.all()
    ph = photographers.objects.all()
    if request.method == "POST" :
        form = galleryForm(request.POST, request.FILES)
        print("+++++++",form.errors)
        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['g_path'])
                form.save()
                return redirect('/photographer/imgtable')
            except:
                print("------------------",sys.exc_info())
                pass
    else:
        form = galleryForm()
    return render(request, "photoimginsert.html", {'form': form, 'cts':ct, 'phs':ph})

def photoimgdelete(request, id):
    deletdata = gallery.objects.get(g_id=id)
    deletdata.delete()
    return redirect("/photographer/imgtable")

def photoimgupdate(request, id):
    a = gallery.objects.get(g_id=id)
    ct = category.objects.all()
    ph = photographers.objects.all()
    return render(request,'photogalleryupdate.html', {'imgs':a, 'cts':ct, 'phs':ph})


def photoeditimg(request, id):
    a = gallery.objects.get(g_id=id)
    form = galleryForm(request.POST, request.FILES, instance=a)
    print("---------",form.errors)
    if form.is_valid():
        handle_uploaded_file(request.FILES['g_path'])
        form.save()
        return redirect("/photographer/imgtable")
    return render(request, 'photogalleryupdate.html', {'imgs': a})

def photographerupdate(request):
    if request.session.has_key('pusername'):
        area = Area.objects.all()
        cat = category.objects.all()
        pk = p_package.objects.all()
        id = request.session['ph_id']
        a = photographers.objects.get(p_id=id)
        return render(request,'photographeredit.html', {'photos':a, 'area':area, 'pkg':pk, 'cat':cat})
    else:
        return render(request, "photographerlogin.html")

def editphotographer(request, id):
    a = photographers.objects.get(p_id=id)
    form = photographerForm(request.POST, request.FILES, instance = a)
    if form.is_valid():
        handle_uploaded_file(request.FILES['p_image'])
        form.save()
        return redirect("/photographer/photohome/")
    print("---------", form.errors)
    return redirect("/photographer/photographerupdate/")


def photoforgot(request):
    return render(request, "photoforgotpassword.html")

def photosendemail(request):
    otp1 = random.randint(10000, 99999)
    e = request.POST['email']
    request.session['temail']=e
    obj = photographers.objects.filter(p_email=e).count()

    print("----------------------",obj)
    if obj == 1:
        val = photographers.objects.filter(p_email=e).update(p_otp=otp1 , p_otp_used=0)
        subject = 'OTP Verification'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]
        send_mail(subject, message, email_from, recipient_list)
        return render(request, 'photoset_password.html')
    else:
        messages.error(request, "This email id is not registered.")
        return render(request, "forgotpassword.html")

def photoset_password(request):
    totp = request.POST['otp']
    tpassword = request.POST['password']
    cpassword = request.POST['cpassword']

    if tpassword == cpassword :
        e = request.session['temail']
        val = photographers.objects.filter(p_email=e, p_otp=totp, p_otp_used=0).count()

        if val == 1:
            val = photographers.objects.filter(p_email=e).update(p_otp_used=1, p_password=tpassword)
            return render(request, "photographerlogin.html")

    return render(request, "photoset_password.html")

def photologout(request):
    try:
        del request.session['pusername']
        del request.session['temail']
    except:
        pass

    return render(request,"photographerlogin.html")