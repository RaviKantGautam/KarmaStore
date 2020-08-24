from django_filters import FilterSet,ChoiceFilter
from django_filters.widgets import *

from .models import *
from django import forms
import django_filters

class Product_Filter(FilterSet):
    name = django_filters.CharFilter(field_name='name',lookup_expr='icontains')
    netprice = django_filters.RangeFilter(lookup_expr='lte',label='Price')
    discount = django_filters.RangeFilter(lookup_expr='lte')
    brand__name = django_filters.ModelChoiceFilter(queryset=Brand.objects.all())
    catid__catname = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    dod = django_filters.BooleanFilter(field_name='dod',widget=BooleanWidget())
    class Meta:
            model = Product
            fields = ['name', 'netprice','discount']
            exclude = ['image']
