from django import forms
from SJMS.models import City
from SJMS.models import Users
from SJMS.models import Area
from SJMS.models import package
from SJMS.models import p_package
from SJMS.models import category
from SJMS.models import contactus
from SJMS.models import gallery
from SJMS.models import Booking
from SJMS.models import photographers
from SJMS.models import feedback


class UserForm(forms.ModelForm):
	class Meta:
		model = Users
		fields = ["user_name", "Email", "password", "contact", "address", "user_gender", "area_id"]


class CityForm(forms.ModelForm):
	class Meta:
		model = City
		fields = ["city_name"]

class AreaForm(forms.ModelForm):
	class Meta:
		model = Area
		fields = ["area_name", "area_pincode", "city_id"]


class p_packageForm(forms.ModelForm):
	class Meta:
		model = p_package
		fields = ["p_pk_name", "p_pk_desc", "p_pk_amount", "p_pk_duration"]


class categoryForm(forms.ModelForm):
	image_path = forms.FileField()
	class Meta:
		model = category
		fields = ["c_name", "c_desc", "image_path"]


class packageForm(forms.ModelForm):
	class Meta:
		model = package
		fields = ["pk_name", "pk_desc", "pk_amount", "c_id"]


class contactForm(forms.ModelForm):
	class Meta:
		model = contactus
		fields = ["cn_name", "cn_desc", "cn_email", "cn_phone"]

class galleryForm(forms.ModelForm):
	class Meta:
		model = gallery
		fields = ["g_path", "c_id", "p_id"]

class bookingForm(forms.ModelForm):
	class Meta:
		model = Booking
		fields = ["b_date", "b_status", "b_amount", "b_desc", "payment_status", "pk_id", "user_id", "p_id"]

class photographerForm(forms.ModelForm):
	class Meta:
		model = photographers
		fields = ["p_name", "p_contact", "p_email", "p_password", "p_address", "p_gender", "p_image", "area_id", "p_pk_id", "p_amt", "p_desc", "c_id"]

class feedbackForm(forms.ModelForm):
	class Meta:
		model = feedback
		fields = ["f_date", "f_desc", "user_id", "p_id"]

