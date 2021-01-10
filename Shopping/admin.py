from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm,AdminPasswordChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core import serializers
from django.db.models import Q

from .form import UserAdminChangeForm, AdminUserCreationForm
from .models import *
from django import forms
from django.core.mail import send_mail
from django.conf import settings
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    admin.AdminSite.site_header = "Shopping MVC"
    admin.AdminSite.site_title = "Shopping MVC"
    admin.AdminSite.index_title = "Shopping MVC Dashboard"
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('id','email', 'admin','staff','client','active','age','phn_no')
    list_filter = ('admin','email')
    fieldsets = (
        ('Credential', {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('admin','staff','client','active')}),
        ('Personal Detail', {'fields': ('name','age','phn_no','pro_pic','background_pic')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}),
    )
    search_fields = ('email','name')
    ordering = ('email','name')
    filter_horizontal = ()

    def has_module_permission(self, request):
        if request.user.is_anonymous:
            return False
        elif request.user.is_admin:
            return True
        else:
            return True

    def has_delete_permission(self, request, obj=None):
        return False

class ProductAdmin(admin.ModelAdmin):
    admin.AdminSite.site_header = "Shopping MVC"
    admin.AdminSite.site_title = "Shopping MVC"
    admin.AdminSite.index_title = "Shopping MVC Dashboard"
    list_display = ('id','name','netprice','discount','product_image','image','brand','catid','supercat','user','create_at','updated_at','changes_done','dod')
    list_filter = ('name','netprice','discount','catid','supercat')
    list_display_links = ('name',)
    list_per_page = 10
    list_max_show_all = 200
    list_editable = ('discount','image','dod','netprice')

    search_fields = ('name','netprice','discount')
    ordering = ('name',)
    filter_horizontal = ()
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = True

    def has_module_permission(self, request):
        if request.user.is_anonymous:
            return False
        elif request.user.is_admin:
            return True
        else:
            return False
    def has_delete_permission(self, request, obj=None):
        if request.user.is_anonymous:
            return False
        elif request.user.is_admin:
            return True
        else:
            return False

class ProductPhotoAdmin(admin.ModelAdmin):
    list_display = ('id','product_image','caption','pid','name','create_at','updated_at')
    list_display_links = ('product_image',)
    list_per_page = 10
    list_max_show_all = 200
    list_editable = ('caption', 'name')
    search_fields = ('pid__name',)
    def has_module_permission(self, request):
        if request.user.is_anonymous:
            return False
        elif request.user.is_admin:
            return True
        else:
            return False
    def has_delete_permission(self, request, obj=None):
        if request.user.is_anonymous:
            return False
        elif request.user.is_admin:
            return True
        else:
            return False

class ProductPropertyAdmin(admin.ModelAdmin):
    list_display = ('id','width','height','depth','weight','color','create_at','updated_at','pid')
    list_display_links = ('id',)
    list_per_page = 10
    list_max_show_all = 200
    list_editable = ('width','height','depth','weight','color')
    def has_module_permission(self, request):
        if request.user.is_anonymous:
            return False
        elif request.user.is_admin:
            return True
        else:
            return False
    def has_delete_permission(self, request, obj=None):
        if request.user.is_anonymous:
            return False
        elif request.user.is_admin:
            return True
        else:
            return False

class StockAdmin(admin.ModelAdmin):
    list_display = ('id','stock','create_at','updated_at','pid')
    list_display_links = ('id',)
    list_per_page = 10
    list_max_show_all = 200
    list_editable = ('stock',)
    def has_module_permission(self, request):
        if request.user.is_anonymous:
            return False
        elif request.user.is_admin:
            return True
        else:
            return False
    def has_delete_permission(self, request, obj=None):
        if request.user.is_anonymous:
            return False
        elif request.user.is_admin:
            return True
        else:
            return False


class billAdmin(admin.ModelAdmin):
    list_display = ('id','datetime','grandtotal','payment_method','city','zipcode','addr','email','status','precieve','cpname','cremark')
    list_display_links = ('id',)
    list_per_page = 10
    list_max_show_all = 200
    def has_module_permission(self, request):
        if request.user.is_anonymous:
            return False
        elif request.user.is_admin:
            return True
        else:
            return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False


class billdetailAdmin(admin.ModelAdmin):
    list_display = ('billid','proid','price','qty')
    list_display_links = ('proid',)
    list_per_page = 10
    list_max_show_all = 200
    def has_module_permission(self, request):
        if request.user.is_anonymous:
            return False
        elif request.user.is_admin:
            return True
        else:
            return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False


class TrackingAdmin(admin.ModelAdmin):
    list_display = ('id','addr','date','status','billid')
    list_display_links = ('id',)
    list_per_page = 10
    list_max_show_all = 200
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        if request.user.is_anonymous:
            return False
        elif request.user.is_staff:
            return True
        else:
            return False
    def has_add_permission(self, request):
        if request.user.is_anonymous:
            return False
        elif request.user.is_staff and not request.user.is_admin:
            return True
        else:
            return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_staff and not request.user.is_admin:
            return Tracking.objects.filter(status='sp')
        return qs

class CouponAdmin(admin.ModelAdmin):
    list_display = ('id','code','price','date_create','expiry_date','user')
    list_display_links = ('code',)
    list_per_page = 10
    list_max_show_all = 200
    list_editable = ('price',)
    def has_module_permission(self, request):
        if request.user.is_anonymous:
            return False
        elif request.user.is_admin:
            return True
        else:
            return False

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','parent','commentbody','date','active','user')
    list_display_links = ('id',)
    list_per_page = 10
    list_max_show_all = 200
    list_editable = ('active','parent')

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_anonymous:
            return False
        elif request.user.is_admin:
            return True
        else:
            return False
    def has_add_permission(self, request):
        return False
    def has_module_permission(self, request):
        if request.user.is_anonymous:
            return False
        elif request.user.is_admin:
            return True
        else:
            return False

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id','name','email','phn','reviewbody','star_rating')
    list_display_links = ('id',)
    list_per_page = 10

    def has_delete_permission(self, request, obj=None):
        # if request.user.is_admin:
        #     return False
        # else:
            return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False
    def has_module_permission(self, request):
        if request.user.is_anonymous:
            return False
        elif request.user.is_admin:
            return True
        else:
            return False

class subscribeAdmin(admin.ModelAdmin):
    def Send_Email(self,request,queryset):
        email=[em.email for em in queryset.all() if em.status==True]
        send_mail('Hi','Today Your are getting 80% discount on shoes of high brands. Shopp now with us',settings.EMAIL_HOST_USER,email)
    list_display = ('email','status','date','lastdate')
    list_display_links = None
    list_editable = ('status',)
    list_per_page = 10
    list_max_show_all = 200
    actions = ['Send_Email']
    def has_view_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        # if User.is_admin or User.is_admin:
        #     return False
        # else:
            return False
    def has_module_permission(self, request):
        if request.user.is_anonymous:
            return False
        elif request.user.is_admin:
            return True
        else:
            return False
    def has_add_permission(self, request):
        return False

class CategoryAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        if request.user.is_anonymous:
            return False
        elif request.user.is_admin:
            return True
        else:
            return False

class BrandAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        if request.user.is_anonymous:
            return False
        elif request.user.is_admin:
            return True
        else:
            return False

#
# admin.site.register(User)
admin.site.register(User,UserAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Brand,BrandAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductPhoto,ProductPhotoAdmin)
admin.site.register(ProductProperty,ProductPropertyAdmin)
admin.site.register(Stock,StockAdmin)
admin.site.register(bill,billAdmin)
admin.site.register(billdetail,billdetailAdmin)
admin.site.register(Tracking,TrackingAdmin)
admin.site.register(subscribe,subscribeAdmin)
admin.site.register(Coupon,CouponAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Review,ReviewAdmin)
admin.site.unregister(Group)
