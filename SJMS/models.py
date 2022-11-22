from django.db import models

# Create your models here.
class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=40)

    class Meta:
        db_table="city"

class Area(models.Model):
    area_id = models.AutoField(primary_key=True)
    area_name = models.CharField(max_length=40)
    area_pincode = models.IntegerField(max_length=10)
    city_id = models.ForeignKey(City, on_delete=models.CASCADE)

    class Meta:
        db_table="area"


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=40)
    Email = models.EmailField()
    password = models.CharField(unique=True,max_length=20)
    contact = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    user_gender = models.CharField(max_length=7)
    area_id = models.ForeignKey(Area, on_delete=models.CASCADE)
    is_admin = models.IntegerField(default=0)
    otp = models.CharField(max_length=10)
    otp_used = models.IntegerField(default=0)

    class Meta:
        db_table="users"


class p_package(models.Model):
    p_pk_id = models.AutoField(primary_key=True)
    p_pk_name = models.CharField(max_length=40)
    p_pk_desc = models.CharField(max_length=200)
    p_pk_amount = models.IntegerField(max_length=10)
    p_pk_duration = models.CharField(max_length=20)

    class Meta:
        db_table="p_package"

class category(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=40)
    c_desc = models.CharField(max_length=200)
    image_path = models.FileField(max_length=100)

    class Meta:
        db_table="category"

class photographers(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_name = models.CharField(max_length=40)
    p_image = models.FileField()
    p_contact =  models.CharField(max_length=10)
    p_email = models.EmailField()
    p_password = models.CharField(unique=True,max_length=20)
    p_address = models.CharField(max_length=200)
    p_gender = models.CharField(max_length=7)
    p_amt = models.IntegerField(max_length=10)
    p_desc = models.CharField(max_length=200)
    c_id = models.ForeignKey(category, on_delete=models.CASCADE)
    area_id = models.ForeignKey(Area, on_delete=models.CASCADE)
    p_pk_id = models.ForeignKey(p_package, on_delete=models.CASCADE)
    p_otp = models.CharField(max_length=10)
    p_otp_used = models.IntegerField()
    pay_status=models.IntegerField(max_length=2,default=0)

    class Meta:
        db_table="photographer"


class gallery(models.Model):
    g_id = models.AutoField(primary_key=True)
    g_path = models.FileField(max_length=100)
    c_id = models.ForeignKey(category, on_delete=models.CASCADE)
    p_id = models.ForeignKey(photographers, on_delete=models.CASCADE)

    class Meta:
        db_table="gallery"

class package(models.Model):
    pk_id = models.AutoField(primary_key=True)
    pk_name = models.CharField(max_length=40)
    pk_desc = models.CharField(max_length=200)
    pk_amount = models.IntegerField(max_length=10)
    c_id = models.ForeignKey(category, on_delete=models.CASCADE)

    class Meta:
        db_table="package"

class feedback(models.Model):
    f_id = models.AutoField(primary_key=True)
    f_date = models.DateField()
    f_desc = models.CharField(max_length=200)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    p_id = models.ForeignKey(photographers, on_delete=models.CASCADE)

    class Meta:
        db_table="feedback"

class Booking(models.Model):
    b_id = models.AutoField(primary_key=True)
    b_date = models.DateField()
    b_desc = models.CharField(max_length=200)
    b_status = models.CharField(max_length=200)
    b_amount = models.IntegerField(max_length=10)
    payment_status = models.CharField(max_length=200)
    pk_id = models.ForeignKey(package, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    p_id = models.ForeignKey(photographers, on_delete=models.CASCADE)

    class Meta:
        db_table="booking"


class contactus(models.Model):
    cn_id = models.AutoField(primary_key=True)
    cn_name = models.CharField(max_length=50)
    cn_email= models.EmailField()
    cn_phone = models.CharField(max_length=12)
    cn_desc = models.CharField(max_length=200)
    class Meta:
        db_table="contactus"