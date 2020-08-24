from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.
from django.core.validators import *
from django.utils.html import format_html
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class UserManager(BaseUserManager):
    def create_user(self,email,password=None):
        if not email:
            raise ValueError('User Must have email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user
    def create_superuser(self,email,password):
        user = self.create_user(email=email,password=password)
        user.active=True
        user.admin=True
        user.staff=True
        user.save(using=self._db)
        return user

def phn_no_validation(value):
    if str(value).isnumeric() == False:
        raise ValidationError('Invalid Mobile Number')
    elif len(str(value)) < 10 or len(str(value)) > 13:
        raise ValidationError('Mobile Number Should be 10 character')
    else:
        return value

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255,unique=True,verbose_name="Email")
    name = models.CharField(max_length=50,verbose_name="Name",null=True,blank=True)
    active = models.BooleanField(default=False)
    age = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)],verbose_name="Age",null=True,blank=True)
    phn_no = models.CharField(max_length=12,verbose_name="Mobile No.",validators=[phn_no_validation],null=True,blank=True)
    pro_pic = models.ImageField(verbose_name="Profile Pic",null=True,blank=True)
    background_pic = models.ImageField(verbose_name="Background Wallpaper",null=True,blank=True)
    client = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        # print('perm: ',perm)
        # return perm == 'Shopping.view'
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        # if self.is_admin:
        #     return True
        # else:
        #     return app_label=='Shopping'
        return True
    @property
    def is_client(self):
        return self.client
    @property
    def is_staff(self):
        return self.staff
    @property
    def is_admin(self):
        return self.admin
    @property
    def is_active(self):
        return self.active
    objects = UserManager()

class Category(models.Model):
    catname = models.CharField(max_length=255, verbose_name="Category Name")
    desc = models.TextField(verbose_name="Description")
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    objects = models.Manager
    def __str__(self):
        return self.catname
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = "Categories"

class Brand(models.Model):
    name = models.CharField(max_length=255, verbose_name="Brand")
    logo = models.ImageField(verbose_name="Logo")
    subdescription = models.TextField(verbose_name="Description")
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    catid = models.ManyToManyField(Category, verbose_name="Category")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    object = models.Manager
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = "Brands"

class Product(models.Model):
    supercatchoice = [("M", "Male"), ("F", "Female"), ("K", "Kids")]
    name = models.CharField(max_length=255, verbose_name="Product Name")
    netprice = models.FloatField(verbose_name="Net Price")
    discount = models.FloatField(verbose_name="Discount")
    desc = models.TextField(verbose_name="Description")
    image = models.ImageField(verbose_name="Image")
    brand = models.ForeignKey(Brand,verbose_name="Brand",on_delete=models.CASCADE)
    catid = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Category")
    supercat = models.CharField(max_length=255, verbose_name="Type", choices=supercatchoice)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name="User")
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    changes_done = models.TextField(verbose_name="Changes Note")
    dod = models.BooleanField(verbose_name="Deal of Day",default=False)
    object = models.Manager
    def __str__(self):
        return self.name
    def product_image(self):
        return format_html('<img src="/static/media/{}" width="100" height="100" alt="no image found" />'.format(self.image))
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = "Products"

class ProductPhoto(models.Model):
    photo = models.ImageField(verbose_name="Product Pics")
    name = models.CharField(max_length=255,verbose_name="Name")
    caption = models.CharField(max_length=255, verbose_name="Caption")
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pid = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    objects = models.Manager
    def __str__(self):
        return self.caption
    def product_image(self):
        return format_html('<img src="/static/media/{}" width="100" height="100" alt="no image found" />'.format(self.photo))

class ProductProperty(models.Model):
    pid = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name="Product")
    width = models.FloatField(verbose_name="Width",validators=[MinValueValidator(0),MaxValueValidator(18)])
    height = models.FloatField(verbose_name="Height",validators=[MinValueValidator(1),MaxValueValidator(10)])
    depth = models.FloatField(verbose_name="Depth",validators=[MinValueValidator(1),MaxValueValidator(10)])
    weight = models.FloatField(verbose_name="Weight",validators=[MinValueValidator(30),MaxValueValidator(300)])
    color = models.CharField(max_length=10,verbose_name="Color(HEX)")
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager
    def __str__(self):
        return str(self.pid)

class Stock(models.Model):
    pid = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name="Product")
    stock = models.IntegerField(verbose_name="Stock",validators=[MinValueValidator(0)])
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.pid)+" : "+str(self.stock)

class Coupon(models.Model):
    code = models.CharField(max_length=50,verbose_name="CODE")
    price = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)],verbose_name="Price")
    date_create = models.DateField(verbose_name="Start Date")
    expiry_date = models.DateField(verbose_name="Expiry Date")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    objects = models.Manager
    def __str__(self):
        return self.code

class bill(models.Model):
    STATUS = [('pd', 'Pending'),('sp', 'Shipping'), ('dp', 'Dispatch'),('cr','Cancel')]
    PAYMENT_CHOICE = [('online','online'),('COD','COD')]
    datetime = models.DateTimeField(auto_now_add=True,verbose_name='Date')
    fname = models.CharField(max_length=255,verbose_name='First Name')
    lname = models.CharField(max_length=255,verbose_name='Last Name')
    grandtotal = models.FloatField(verbose_name='GrandTotal')
    payment_method = models.CharField(max_length=255,verbose_name='Payment Type',choices=PAYMENT_CHOICE,default=PAYMENT_CHOICE[0])
    city = models.CharField(max_length=255,verbose_name='City')
    zipcode = models.PositiveIntegerField(verbose_name='Zipcode')
    addr= models.TextField(verbose_name='Address')
    phn = models.IntegerField(verbose_name='Mobile Number')
    email = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name='Email')
    status = models.CharField(max_length=255,verbose_name='Status',blank=True,null=True,choices=STATUS,default=STATUS[0])
    cancel = models.BooleanField(verbose_name="Cancelled Status",default=False)
    precieve = models.CharField(max_length=255,verbose_name='Person Recieve',blank=True,null=True)
    cpname = models.CharField(max_length=255,verbose_name='Company',blank=True,null=True)
    GST = models.FloatField(verbose_name="GST Tax",default=18.5)
    nettotal = models.FloatField(verbose_name="Net Total",blank=True,null=True)
    discounted_price = models.FloatField(verbose_name="Discounted Total",blank=True,null=True)
    cremark = models.TextField(blank=True,null=True)
    coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE,verbose_name='Apply Coupon',null=True,blank=True)
    objects = models.Manager
    def __str__(self):
        return str(self.id)
    class Meta:
        ordering = ('-datetime',)

class billdetail(models.Model):
    price = models.FloatField(verbose_name='Price')
    netprice = models.FloatField(verbose_name="Net Price")
    discount = models.FloatField(verbose_name="Discount")
    qty = models.IntegerField(verbose_name='Quantity')
    proid = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='Product Id')
    billid = models.ForeignKey(bill,on_delete=models.CASCADE,verbose_name='Bill ID')
    create_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)

class Tracking(models.Model):
    st = [('sp','Shipping'),('dp','Dispatch')]
    addr = models.TextField(verbose_name='Address')
    date = models.DateTimeField(verbose_name='Date',auto_now_add=True)
    status = models.CharField(verbose_name='Status',choices=st,max_length=255)
    billid = models.ForeignKey(bill,on_delete=models.CASCADE)
    objects = models.Manager
    def __str__(self):
        return str(self.id)

class subscribe(models.Model):
    email = models.EmailField(verbose_name='Email',unique=True,primary_key=True)
    status = models.BooleanField(default=True,verbose_name='Active')
    date = models.DateTimeField(auto_now_add=True,verbose_name='Date')
    lastdate = models.DateTimeField(auto_now=True,verbose_name='Date')
    objects = models.Manager
    def __str__(self):
        return self.email
#
# @receiver(post_save,sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender,instance=None,created=False,**kwargs):
#     if created:
#         Token.objects.create(user=instance)


class Comment(models.Model):
    pid = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='pid')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user',null=True,blank=True)
    commentbody = models.TextField(verbose_name="Comment")
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date')
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self',null=True,blank=True,related_name="reply",on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id)
    class Meta:
        ordering = ('date',)

class Review(models.Model):
    pid = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    name = models.CharField(max_length=255,verbose_name='Name',blank=True,null=True)
    email = models.EmailField(verbose_name='user',blank=True,null=True)
    phn = models.IntegerField(verbose_name='Phone number',validators=[phn_no_validation],blank=True,null=True)
    reviewbody = models.TextField(verbose_name="Review")
    star_rating = models.PositiveIntegerField(verbose_name="Ratings")
    objects = models.Manager
    def __str__(self):
        return self.email
