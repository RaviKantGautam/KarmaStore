from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from Shopping.models import Product, User, bill, Category
from Shopping.ShoppingAPI.serializers import ProductSerializer, RegistrationSerializer, AccountPropertiesSerializer, \
    BillSerializer
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter,OrderingFilter


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def product_detail_view(request, pk):
    # print('here')
    try:
        pd = Product.objects.get(pk=pk,user=User.objects.get(email=Token.objects.get(key=request.headers['Authorization'].lstrip('Token ')).user))
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProductSerializer(pd)
        # print(serializer.data)
        return Response(data=serializer.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def product_update_view(request, pk):
    try:
        pd = Product.objects.get(pk=pk,user=User.objects.get(email=Token.objects.get(key=request.headers['Authorization'].lstrip('Token ')).user))
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user = request.user
    if request.method == 'PUT':
        serializer = ProductSerializer(pd, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # print(serializer)
            data = {'success', 'updated successfully'}
        else:
            data = {'fail', 'update unsuccessful'}
        return Response(data=data)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def product_delete_view(request, pk):
    try:
        pd = Product.objects.get(pk=pk,user=User.objects.get(email=Token.objects.get(key=request.headers['Authorization'].lstrip('Token ')).user))
        # print(pd)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user = request.user
    if request.method == 'DELETE':
        operation = pd.delete()
        if operation:
            data = {'success', 'deleted successfully'}
        else:
            data = {'fail', 'deleted Fail'}
        return Response(data=data)


@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def product_create_view(request):
    user = User.objects.get(email=Token.objects.get(key=request.headers['Authorization'].lstrip('Token ')).user)
    cat = Category.objects.get(pk=3)
    pd = Product(catid=cat)
    pd.name = 'UpdateApiCreateView'
    if user.is_authenticated and request.method=='POST':
        serialize = ProductSerializer(pd, data=request.data)
        # print(serialize)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=status.HTTP_201_CREATED)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST',])
def registration_view(request):
    if request.method=='POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            data = {'response':'successfully registered','email':account.email,'token':Token.objects.get(user=account).key}
        else:
            data = serializer.errors
        return Response(data)

class ApiProductView(ListAPIView):
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination                                   #www.localhost.com/funcClass/urlroute?page=1
    filter_backends = (SearchFilter,OrderingFilter)                           #www.localhost.com/funcClass/urlroute?search=data&ordering=columnname                  add -columnname in case of decendong order
    search_fields = ('name','subid__subcatname')

    def get_queryset(self):
        queryset = Product.objects.filter(user=self.request.user)
        # queryset = Product.objects.filter(user=User.objects.get(email='ravikantgautamjazz@outlook.com'))
        return queryset


class ApiBillView(ListAPIView):
    queryset = bill.objects.all()
    serializer_class = BillSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination                                   #www.localhost.com/funcClass/urlroute?page=1
    filter_backends = (SearchFilter,OrderingFilter)                           #www.localhost.com/funcClass/urlroute?search=data&ordering=columnname                  add -columnname in case of decendong order
    search_fields = ('email__email','datetime')

class UsrApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = AccountPropertiesSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination                                   #www.localhost.com/funcClass/urlroute?page=1
    filter_backends = (SearchFilter,OrderingFilter)                           #www.localhost.com/funcClass/urlroute?search=data&ordering=columnname                  add -columnname in case of decendong order
    search_fields = ('email','id')

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def usrapi(request,pk):
    try:
        pd = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = AccountPropertiesSerializer(pd)
        # print(serializer.data)
        return Response(data=serializer.data)

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def bill_detail_view(request, pk):
    try:
        pd = bill.objects.get(pk=pk)
    except bill.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = BillSerializer(pd)
        # print(serializer.data)
        return Response(data=serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def account_property_view(request):
    try:
        account = request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        serializer = AccountPropertiesSerializer(account)
        return Response(serializer.data)

@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def update_account_view(request):
    try:
        account = request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='PUT':
        serializer = AccountPropertiesSerializer(account,data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = "Account updated Successfully"
            return Response(data=data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
