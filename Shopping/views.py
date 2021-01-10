from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse, QueryDict,HttpResponse
from django.contrib import messages
from Shopping.filter import *
from django.core.mail import send_mail
import requests
from django.utils.decorators import method_decorator
from .decorators import unauthenticated_user
from .form import *
from .models import *
from django.views.generic import *
from django.db.models import Q
from cart.cart import *
from django.core import serializers
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
import random


# import logging
# logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    data = Product.objects.all()
    latest = data[:8]
    coming = data[:8:-1]
    dod = Product.objects.filter(dod=True)[:9]
    return render(request, 'index.html',
                  {'context': latest, 'coming': coming, 'dod': dod, "brand": Brand.objects.all()[2:7]})


def ContactUs(request):
    if request.method == 'POST':
        # 'python -m smtpd -n -c DebuggingServer localhost:1025'
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = "Hi " + str(name) + ","
        message += request.POST['message']
        st = send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[email],
                       fail_silently=False, html_message='<div style="font-size=3rem">' + message + '</h1>')
        # print(st)
        # sp = mail_admins(subject,message,fail_silently=False)
        # print(sp)
        # spt = mail_managers(subject,message,fail_silently=False)
        # print(spt)
        return render(request, 'contact.html', {'message': 'message sended succesfully'})
    return render(request, 'contact.html')


@unauthenticated_user
def loginUser(request):
    if request.method == 'POST':
        next = QueryDict(request.META['QUERY_STRING']).get('next') or '/Shopping'
        # print('servername',request.META['SERVER_NAME'])
        # print('remote name',request.META['REMOTE_HOST'])
        # print('querystring',request.META['QUERY_STRING'])
        # print('httpuseragent',request.META['HTTP_USER_AGENT'])
        # print('serverport',request.META['SERVER_PORT'])
        # print('fullpath',request.get_full_path())
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None and user.is_client and user.is_active:
                login(request, user)
                if not request.POST.get('selector', None):
                    settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
                request.session['client'] = {'email': email}
                messages.success(request, 'Successfully Login')
                return HttpResponseRedirect(next)
            elif user is not None and user.is_staff and user.is_active:
                login(request, user)
                if not request.POST.get('selector', None):
                    settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
                request.session['staff'] = {'email': email}
                messages.success(request, 'Successfully Login')
                return redirect('Shopping:login')
            else:
                messages.error(request, 'Invalid Credentials')
        else:
            messages.error(request, 'Form not Valid')
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@unauthenticated_user
def signupform(request):
    if request.method == 'POST':
        next = QueryDict(request.META['QUERY_STRING']).get('next') or '/Shopping'
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            login(request, user)
            request.session['client'] = {'email': email}
            return HttpResponseRedirect(next)
    else:
        form = RegisterForm()
    return render(request, 'registration.html', {'form': form})


def UserLogout(request):
    next = QueryDict(request.META['QUERY_STRING']).get('next') or '/Shopping'
    try:
        request.session['client'] = ""
        del request.session['client']
        logout(request)
    except:
        pass
    return HttpResponseRedirect(next)

def AllProduct(request):
    context = {}
    context['filter'] = Product_Filter(request.GET, queryset=Product.objects.all())
    pagination_filtered = Paginator(Product_Filter(request.GET, queryset=Product.objects.all()).qs, 12)
    page_number = request.GET.get('page')
    try:
        product_page_obj = pagination_filtered.get_page(page_number)
    except PageNotAnInteger:
        product_page_obj = pagination_filtered.get_page(1)
    except EmptyPage:
        product_page_obj = pagination_filtered.get_page(page_number)
    context['object_list'] = product_page_obj
    return render(request, 'AllProduct.html', context)


class product_search(ListView):
    model = Product
    template_name = 'AllProduct.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        result = super(product_search, self).get_queryset()
        query = self.request.GET.get('searchbar')
        if query:
            productdata = Product.objects.filter(
                Q(name__icontains=query) | Q(brand__name__icontains=query) | Q(catid__catname=query) | Q(
                    supercat__icontains=query[0])).distinct()
            result = productdata
        else:
            result = None
        return result


def categorydata(request):
    data = serializers.serialize("json", Brand.objects.all())
    return HttpResponse(data, content_type='json/text')


# @login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)

    return HttpResponse(len(request.session[settings.CART_SESSION_ID]))


# @login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return HttpResponse('success')


# @login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    total = request.session['cart'][str(id)]['total']
    qty = request.session['cart'][str(id)]['quantity']
    request.session['grandtotal'] = cart.get_grandtotal()
    data = {'total': total, 'qty': qty, 'grandtotal': cart.get_grandtotal()}
    return JsonResponse(data, safe=False)


# @login_required(login_url="/users/login")
def item_increment_qty(request, id, qty):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product, quantity=qty)
    return HttpResponse('/Shopping/Detail/' + str(id))


# @login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    qty = request.session['cart'][str(id)]['quantity']
    if 'coupon' in request.session:
        request.session['grandtotal'] = cart.get_grandtotal() - request.session['coupon']['price']
    else:
        request.session['grandtotal'] = cart.get_grandtotal()
    total = request.session['cart'][str(id)]['total']
    data = {'total': total, 'qty': qty, 'grandtotal': cart.get_grandtotal()}
    return JsonResponse(data, safe=False)


# @login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return HttpResponseRedirect('Shopping:cart/cart-detail/')


# @login_required(login_url="/users/login")
def cart_detail(request):
    if 'cart' in request.session:
        cart = Cart(request)
        if len(request.session['cart']) > 0:
            if 'coupon' in request.session:
                request.session['grandtotal'] = cart.get_grandtotal() - request.session['coupon']['price']
            else:
                request.session['grandtotal'] = cart.get_grandtotal()
            return render(request, 'cart.html', {'total': cart.get_grandtotal()})
        return HttpResponseRedirect('/Shopping')
    return HttpResponseRedirect('/Shopping')


@login_required(login_url='/Shopping/login')
def checkout_form(request):
    if 'cart' in request.session:
        if request.method == 'POST':
            try:
                cart = Cart(request)
                if 'coupon' in request.session:
                    coupon = Coupon.objects.get(pk=request.session['coupon'])
                    b1 = bill(fname=request.POST['fname'],
                              lname=request.POST['lname'],
                              grandtotal=float(request.session['grandtotal']),
                              payment_method=request.POST['pytp'],
                              city=request.POST['city'],
                              zipcode=request.POST['zip'],
                              addr=request.POST['addr'],
                              phn=int(request.POST['phn']),
                              email=request.user,
                              GST=18.0,
                              nettotal=round(cart.get_grandtotal() - (cart.get_grandtotal() * 0.18), 2),
                              discounted_price=float(request.session['grandtotal']),
                              coupon=coupon)
                else:
                    b1 = bill(fname=request.POST['fname'],
                              lname=request.POST['lname'],
                              grandtotal=float(request.session['grandtotal']),
                              payment_method=request.POST['pytp'],
                              city=request.POST['city'],
                              zipcode=request.POST['zip'],
                              addr=request.POST['addr'],
                              phn=int(request.POST['phn']),
                              email=request.user,
                              GST=18.0,
                              nettotal=round(cart.get_grandtotal() - (cart.get_grandtotal() * 0.18), 2),
                              discounted_price=float(request.session['grandtotal']))
                try:
                    b1.save()
                    for key in dict(request.session['cart']):
                        b2 = billdetail(price=request.session['cart'][key]['total'],
                                        netprice=float(request.session['cart'][key]['price']),
                                        discount=request.session['cart'][key]['discount'],
                                        qty=request.session['cart'][key]['quantity'],
                                        proid_id=request.session['cart'][key]['product_id'], billid=b1)
                        b2.save()
                    return HttpResponse(b1.id)
                    # return JsonResponse({'message':'Data is not Correct','gt':gt},content_type='json/text')
                except Exception as e:
                    print('error', e)
                    return HttpResponse('Must Fill the required Field')
            except Exception as e:
                print('error', e)
                return HttpResponse('Must Fill the required Field')
        return render(request, 'checkout.html')
    return HttpResponseRedirect('/Shopping')


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("cp1252")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


@login_required(login_url='/Shopping/login')
def thanksyou(request):
    cart = Cart(request)
    if 'grandtotal' in request.session:
        del request.session['grandtotal']
    if 'coupon' in request.session:
        del request.session['coupon']
    cart.clear()
    billid = request.GET['billid']
    orderbill = bill.objects.get(id=billid)
    orderbilldetail = billdetail.objects.filter(billid=billid)
    context = {'billid': billid, 'orderbill': orderbill, 'orderbilldetail': orderbilldetail}
    action = request.GET.get('action') or None
    if action != None:
        if action == 'viewpdf':
            pdf = render_to_pdf('../templates/confirmpdf.html', context)
            return HttpResponse(pdf, content_type='application/pdf')
        elif action == 'downloadpdf':
            pdf = render_to_pdf('../templates/confirmpdf.html', context)
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = 'Invoice_{}.pdf'.format(str(random.randint(10000, 99999)))
            content = "attachment; filename={}".format(filename)
            response['Content-Disposition'] = content
            return response
    return render(request, 'confirmation.html', context)


class MyAccount(ListView):
    model = bill
    template_name = 'myaccount.html'
    context_object_name = 'billobj'
    paginate_by = 10

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MyAccount, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return bill.objects.filter(email=self.request.user)


def billdetailspage(request, id):
    data = serializers.serialize('json', billdetail.objects.filter(billid=id))
    return HttpResponse(data, content_type='json/text')


class TrackingView(ListView):
    model = Tracking
    template_name = 'tracking.html'
    context_object_name = 'data'

    def get_queryset(self):
        result = super(TrackingView, self).get_queryset()
        order = self.request.GET.get('order')
        email = self.request.GET.get('email')
        if order and email:
            email = User.objects.get(email=email)
            productdata = Tracking.objects.filter(billid=order, billid__email=email)
            result = productdata
        else:
            result = None
        return result


def newsupdate(request):
    if request.method == 'POST':
        nwem = request.POST['nwem']
        next = QueryDict(request.META['QUERY_STRING']).get('next') or '/Shopping'
        try:
            mg = f'''<!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Subscriber</title>
    </head>
    <body>
    <div style="font-size: 3rem;font-weight: bolder;color: #ec5757">Thanks You for your contribution. <br> Your get to you the latest update regarding about the products and services nad discount</div>
    <p>If you want to <a href="http://127.0.0.1:8000/Shopping/unsubscribe?email={nwem}" target="_blank" data-saferedirecturl="https://www.google.com/url?q=/127.0.0.1:8000/Shopping/unsubscribe?email={nwem}">unsubscribe</a> us.Click on!</p>
    </body>
    </html>'''
            print(mg)
            gt = send_mail('Subscriber',
                           'Thanks You for your contribution. Your get to you the latest update regarding about the products and services nad discount',
                           settings.EMAIL_HOST_USER, [nwem], html_message=mg)
            print(gt)
            sub = subscribe(email=nwem)
            sub.save()
        except:
            pass
        return HttpResponseRedirect(next, {'message': 'Thank you for subscribing'})


def unsubscribe(request):
    email = request.GET['email']
    mg = f'''<!doctype html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport"
                  content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <title>Subscriber</title>
        </head>
        <body>
        <div style="font-size: 5rem;font-weight: bolder;color: #ec5757">Thanks You for your contribution. <br> Your get to you the latest update regarding about the products and services nad discount</div>
        <p>If you want to <a href="127.0.0.1:8000/Shopping/unsubscribe?email={email}">unsubscribe</a> us.Click on!</p>
        </body>
        </html>'''
    ft = get_object_or_404(subscribe, email=email)
    ft.status = False
    ft.save()
    send_mail('Unsubscribe',
              'You have Successfully Unsubcribe from Karma Store. You woulf not going to see any updates regarding to it.',
              settings.EMAIL_HOST_USER, [email], html_message=mg)
    return HttpResponseRedirect('/Shopping/')


class APIview(View):
    def get(self, request):
        return render(request, 'APILogin.html')

    def post(self, request):
        if request.method == 'POST':
            auth = authenticate(email=request.POST['email'], password=request.POST['password'])
            if auth is not None:
                print('true')
                print(request.POST['token'])
                tk = Token.objects.get(key=request.POST['token'])
                print(tk)
                acc = {'token': tk, 'url': 'http://127.0.0.1:8000/Shopping/accDetail?key=tk&act=value', 'method': 'GET',
                       'act': 1, 'delete': 'http://127.0.0.1:8000/Shopping/ShoppingAPI/<pk>/delete/'}
                prd = {'token': tk, 'url': 'http://127.0.0.1:8000/Shopping/accDetail?key=tk&act=value', 'method': 'GET',
                       'act': 2,
                       'delete': {'url': 'http://127.0.0.1:8000/Shopping/ShoppingAPI/<pk>/delete', 'method': 'DELETE'},
                       'detail': {'url': 'http://127.0.0.1:8000/Shopping/ShoppingAPI/<pk>/', 'method': 'GET'},
                       'update': {'url': 'http://127.0.0.1:8000/Shopping/ShoppingAPI/<pk>/update', 'method': 'PUT'},
                       'create': {'url': 'http://127.0.0.1:8000/Shopping/ShoppingAPI/create', 'method': 'POST'}}
                billapi = {'token': tk, 'url': 'http://127.0.0.1:8000/Shopping/accDetail?key=tk&act=value',
                           'method': 'GET', 'act': 3,
                           'detail': {'url': 'http://127.0.0.1:8000/Shopping/ShoppingAPI/bill_detail_view/<pk>/',
                                      'method': 'GET'}}
                usr = {'token': tk, 'url': 'http://127.0.0.1:8000/Shopping/accDetail?key=tk&act=value', 'method': 'GET',
                       'act': 4,
                       'detail': {'url': 'http://127.0.0.1:8000/Shopping/ShoppingAPI/usrapi/<pk>/', 'method': 'GET'}}

                return render(request, 'APIview.html', {'acc': acc, 'prd': prd, 'bill': billapi, 'usr': usr})
            else:
                data = {'error': "Credential doesn't match"}
                return render(request, 'APILogin.html', {'context': data})


class APIviewSignUp(View):
    def get(self, request):
        return render(request, 'APISignUp.html')

    def post(self, request):
        if request.method == 'POST':
            auth = authenticate(email=request.POST['email'], password=request.POST['password'])
            if auth is not None:
                tk = Token.objects.get_or_create(user=auth)
                send_mail('Token', 'You Token is ' + str(tk[0]), settings.EMAIL_HOST_USER,
                          ['ravikantgautamjazz@outlook.com'])
                messages.success(request,"Token is sended to your email account:" + str(request.POST['email']))
                return HttpResponseRedirect('http://127.0.0.1:8000/Shopping/APIview')
            else:
                data = {'error': "Credential doesn't match"}
                return render(request, 'APISignUp.html', {'context': data})


def accDetail(request):
    url = request.get_raw_uri()
    print(url)
    try:
        act = request.GET['act']
        key = request.GET['key']
    except:
        raise ValueError('Must fill the credentials')
    headers = {
        'Authorization': 'Token {}'.format(key),
        'Content-Type': 'application/json; charset=utf-8'
    }
    if act == "1":
        r = requests.get(url='http://127.0.0.1:8000/Shopping/ShoppingAPI/acc_properties', headers=headers)
        files = r.json()
        # print(r)
        return JsonResponse(files, safe=False)
    elif act == "2":
        data = ''
        parm = {'page': QueryDict(request.META['QUERY_STRING']).get('page') or None,
                'ordering': QueryDict(request.META['QUERY_STRING']).get('ordering') or None,
                'search': QueryDict(request.META['QUERY_STRING']).get('search') or None}
        for key, value in parm.items():
            if value != None:
                data += '&' + key + "=" + value
        if data != '':
            r = requests.get(url='http://127.0.0.1:8000/Shopping/ShoppingAPI/prdview?' + str(data), headers=headers)
        else:
            r = requests.get(url='http://127.0.0.1:8000/Shopping/ShoppingAPI/prdview', headers=headers)
        files = r.json()
        return JsonResponse(files, safe=False)
    elif act == '3':
        data = ''
        parm = {'page': QueryDict(request.META['QUERY_STRING']).get('page') or None,
                'ordering': QueryDict(request.META['QUERY_STRING']).get('ordering') or None,
                'search': QueryDict(request.META['QUERY_STRING']).get('search') or None}
        for key, value in parm.items():
            if value != None:
                data += '&' + key + "=" + value
        if data != '':
            r = requests.get(url='http://127.0.0.1:8000/Shopping/ShoppingAPI/billapi?' + str(data), headers=headers)
        else:
            r = requests.get(url='http://127.0.0.1:8000/Shopping/ShoppingAPI/billapi', headers=headers)
        print(r)
        files = r.json()
        return JsonResponse(files, safe=False)
    elif act == '4':
        data = ''
        parm = {'page': QueryDict(request.META['QUERY_STRING']).get('page') or None,
                'ordering': QueryDict(request.META['QUERY_STRING']).get('ordering') or None,
                'search': QueryDict(request.META['QUERY_STRING']).get('search') or None}
        for key, value in parm.items():
            if value != None:
                data += '&' + key + "=" + value
        if data != '':
            r = requests.get(url='http://127.0.0.1:8000/Shopping/ShoppingAPI/UsrApiView?' + str(data), headers=headers)
        else:
            r = requests.get(url='http://127.0.0.1:8000/Shopping/ShoppingAPI/UsrApiView', headers=headers)
        print(r)
        files = r.json()
        return JsonResponse(files, safe=False)
    else:
        raise ValueError('Must fill the credentials')


def wistlist_add(request, id):
    try:
        data = Product.objects.get(id=id)
        lt = []
        if 'wishlist' in request.session:
            lt = list(request.session['wishlist'])
            for k in lt:
                if k['id'] == id:
                    # print(k['id'])
                    break
            else:
                d = {
                    'id': data.id,
                    'name': data.name,
                    'price': data.netprice,
                    'discount': data.discount,
                    'desc': data.desc,
                    'pic': data.image.name,

                }
                lt.append(d)
        else:

            d = {
                'id': data.id,
                'name': data.name,
                'price': data.netprice,
                'discount': data.discount,
                'desc': data.desc,
                'pic': data.image.name,

            }
            lt.append(d)
        # print(lt)
        request.session['wishlist'] = lt
        return HttpResponse(len(lt))
    except Product.DoesNotExist:
        raise ValueError('Product not exist')


def wistlist_detail(request):
    next = QueryDict(request.META['QUERY_STRING']).get('next') or '/Shopping'
    if 'wishlist' in request.session:
        if len(request.session['wishlist']) > 1:
            return render(request, 'wistlistdetail.html')
        else:
            return HttpResponseRedirect(next)
    else:
        return HttpResponseRedirect(next)


def remove_wishlist_item(request, id):
    next = QueryDict(request.META['QUERY_STRING']).get('next') or '/Shopping'
    try:
        lt = []
        count = 0
        if 'wishlist' in request.session:
            lt = list(request.session['wishlist'])
            for k in lt:
                if k['id'] == id:
                    del lt[count]
                    break
                else:
                    count += 1
        request.session['wishlist'] = lt
        return HttpResponseRedirect(next)
    except Product.DoesNotExist:
        raise ValueError('Product not exist')


def wishlistdeleteall(request):
    next = QueryDict(request.META['QUERY_STRING']).get('next') or '/Shopping'
    try:
        request.session['wishlist'] = ''
        del request.session['wishlist']
        return HttpResponseRedirect(next)
    except:
        return HttpResponseRedirect(next)


def compareList_add(request, id):
    try:
        data = Product.objects.get(id=id)
        lt = []
        if 'compareList' in request.session:
            lt = list(request.session['compareList'])
            for k in lt:
                if k['id'] == id:
                    # print(k['id'])
                    break
            else:
                d = {
                    'id': data.id,
                    'name': data.name,
                    'price': data.netprice,
                    'discount': data.discount,
                    'desc': data.desc,
                    'pic': data.image.name,

                    'subid': data.brand.name
                }
                lt.append(d)
        else:

            d = {
                'id': data.id,
                'name': data.name,
                'price': data.netprice,
                'discount': data.discount,
                'desc': data.desc,
                'pic': data.image.name,

                'subid': data.brand.name
            }
            lt.append(d)
        # print(lt)
        request.session['compareList'] = lt
        return HttpResponse(len(lt))
    except Product.DoesNotExist:
        raise ValueError('Product not exist')


def compareList_detail(request):
    next = QueryDict(request.META['QUERY_STRING']).get('next') or '/Shopping'
    if 'compareList' in request.session:
        if len(request.session['compareList']) > 1:
            return render(request, 'compareList.html')
        else:
            return HttpResponseRedirect(next)
    else:
        return HttpResponseRedirect(next)


def compareListdeleteall(request):
    next = QueryDict(request.META['QUERY_STRING']).get('next') or '/Shopping'
    try:
        request.session['compareList'] = ''
        del request.session['compareList']
        return HttpResponseRedirect(next)
    except:
        return HttpResponseRedirect(next)


def ForgetEmail(request):
    email = request.GET.get('email')
    try:
        emailus = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        emailus = None
    print(emailus)
    if emailus != None:
        send_mail(subject='Forget Account Password For Karma Store',
                  message='Click this link to change your password : ', from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[email],
                  fail_silently=False,
                  html_message=f'<h3>Click this link to change your password : <a href="http://127.0.0.1:8000/Shopping/forgetPasswordPage?email={email}">Change Password Page</a></h3>')
    # print(st)
    respn = ""
    if emailus != None:
        respn = "message sended successfully"
    else:
        respn = "Error sending: Either Your email is incorrect or Your are not a registered user"
    return HttpResponse(respn)


@login_required(login_url='/Shopping/login')
def change_password(request):
    if request.method == 'POST':
        form = clientChangePassword(request.user, request.POST)
        if form.is_valid():
            print('here')
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/Shopping')
        else:
            messages.error(request, "Credential doesn't match")
    else:
        form = clientChangePassword(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


def forgetPasswordPage(request):
    email = request.GET.get('email')
    print(email)
    if request.method == 'POST':
        emailps = request.POST.get('emailps')
        changedone = True
        try:
            us = User.objects.get(email__iexact=emailps)
            print(us)
        except User.DoesNotExist:
            changedone = False
        if changedone == True:
            us.set_password(request.POST.get('password2'))
            us.save()
            messages.success(request, "Password Change Successfully. Now You Can login Using New Credentials")
        else:
            messages.error(request, 'Fail to Change Password')
        return redirect('Shopping:login')
    return render(request, 'forgetchangepassword.html', {'email': email})


def applyCouponCode(request):
    code = request.GET['code']
    try:
        appcode = Coupon.objects.get(code__iexact=code)
        grandtotal = request.session['grandtotal']
        grandtotal -= appcode.price
        request.session['grandtotal'] = grandtotal
        request.session['coupon'] = appcode.pk
    except Coupon.DoesNotExist:
        return HttpResponse("error")
    return HttpResponse(grandtotal)


@login_required(login_url='/Shopping/login')
def cancelorder(request):
    id = request.GET.get('id')
    reason = request.GET.get('reason')
    data = bill.objects.get(id=id)
    data.status = 'cr'
    data.cremark = reason
    data.save()
    return HttpResponse('success')


@login_required(login_url='/Shopping/login')
def myprofile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('Shopping:myprofile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'myprofile.html', {'form': form})


class staff_profile(View):
    def get(self, request):
        # data = bill.objects.filter(~Q(status='cr'))
        data = bill.objects.all()
        print(data)
        form = TrackingForm()
        return render(request, 'staff_profile.html', {'context': data})


def staff_profile_update(request, id):
    return HttpResponse('success')


def review(request):
    if request.is_ajax():
        # print('yes')
        # print(request.POST)
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('success')
        else:
            # print(form.errors)
            return HttpResponse(form.errors)
    else:
        return HttpResponse('Wrong Method')


@login_required(login_url='/Shopping/login')
def comment(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        parent_obj = None
        try:
            parent_id = int(request.POST.get('parent_id'))
            # print(parent_id)
        except:
            parent_id = None
        if parent_id != None:
            parent_qs = Comment.objects.get(id=parent_id)
            # print(parent_qs)
            if parent_qs:
                parent_obj = parent_qs
        if parent_obj:
            form.parent_id = parent_obj
        getdata,data = Comment.objects.get_or_create(user=request.user, pid=form.cleaned_data.get('pid'),
                                      commentbody=form.cleaned_data.get('commentbody'),parent=parent_obj)
        newdata = serializers.serialize('json',Comment.objects.filter(id=getdata.id))
        return HttpResponse(newdata)
    else:
        return HttpResponse(form.errors)

def loadcomment(request):
    if request.is_ajax() and request.method=='GET':
        context = Comment.objects.filter(pid=request.GET.get('pid'))
        data = serializers.serialize('json',context)
        return HttpResponse(data)

class Node:
    def __init__(self,data):
        self.head = None
        self.data = data
    def printData(self):
        return self.data

def commentpage(request):
    data = Comment.objects.all()
    lt = []
    print(len(data))
    i=0
    while len(data):
        # print(i.parent)
        if i == len(data):
            break
        com = Node(data[i])
        if data[i].parent != None:
            temp = Node(data[i].parent)
            com.head = temp
            i+=1
        else:
            i+=1
        lt.append(com)
    return render(request,'demo.html',{'context':lt[::-1]})


def Detail(request, pk):
    prd = Product.objects.get(pk=pk)
    disc = int(prd.netprice) - int(prd.netprice) * (int(prd.discount) / 100)
    try:
        reviewdata = Review.objects.filter(pid=pk)
        if reviewdata.count() < 1:
            reviewdata = None
    except Review.DoesNotExist:
        reviewdata = None
    try:
        commentdata = Comment.objects.filter(pid=pk)
        if commentdata.count() < 1:
            commentdata = None
    except Comment.DoesNotExist:
        commentdata = None
    print(commentdata)
    return render(request, 'single-product.html',
                  {'object': prd, 'stock': Stock.objects.get(pid=pk), 'spec': ProductProperty.objects.get(pid=pk),
                   'saleprice': disc, 'reviewdata': reviewdata, 'comment': commentdata})

class Term_Condition(TemplateView):
    template_name = 'term&condition.html'

class Policy(TemplateView):
    template_name = 'policy.html'
