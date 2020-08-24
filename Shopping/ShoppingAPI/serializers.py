from rest_framework import serializers
from Shopping.models import Product,User,bill

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = ['id','name','price','stock','discount','desc','product_image','subid']
        fields = '__all__'
    def create(self, validated_data):
        return Product.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.price = validated_data.get('price',instance.price)
        instance.stock = validated_data.get('stock',instance.stock)
        instance.discount = validated_data.get('discount',instance.discount)
        instance.desc = validated_data.get('desc',instance.desc)
        instance.product_image = validated_data.get('product_image',instance.product_image)
        instance.subid = validated_data.get('subid',instance.subid)
        instance.save()
        return instance

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['email','password','password2']
        extra_kwargs={
            'password':{"write_only":True}
        }
    def save(self, **kwargs):
        account = User(
            email=self.validated_data['email']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password':'Passwords must match'})
        account.set_password(password)
        account.save()
        return account

class AccountPropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk','email','is_client','is_admin','is_staff','is_active']


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = bill
        # fields = ['id','datetime','grandtotal','payment_method','city','zipcode','addr','email','status','precieve','cpname','cremark']
        fields = '__all__'

