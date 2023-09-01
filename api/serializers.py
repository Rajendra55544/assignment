from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from .models import UserUploads,Address
User = get_user_model()

class UsersRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    class Meta:
        model = User
        fields = ('name','email','password')
        extra_kwargs = {'name': {'required': True},'password': {'required': True} } 
    
    def create(self, validated_data, *args, **kwargs):
        user = User.objects.create_user(username=validated_data['email'],is_active=True,**validated_data)
        return user
 

class UsersLoginSerializer(serializers.ModelSerializer):
  
    def validate(self, data):
        user = authenticate(**data)  #here Authicate check email and password are correct or not
        if user and user.is_active and not user.is_superuser:   # here check user is active or not
            user.user_id = user.id
            return user
        raise serializers.ValidationError("Incorrect Credentials")

    class Meta:
        model = User
        fields = ['email','password']
        extra_kwargs = {'email': {'required': True}} 

class AdminLoginSerializer(serializers.ModelSerializer):
  
    def validate(self, data):
        user = authenticate(**data)  #here Authicate check email and password are correct or not
        if user and user.is_active and user.is_superuser:   # here check user is active or not
            return user
        raise serializers.ValidationError("Incorrect Credentials")

    class Meta:
        model = User
        fields = ['email','password']
        extra_kwargs = {'email': {'required': True}} 


class Uploadfile(serializers.ModelSerializer):
    class Meta:
        model = UserUploads
        fields  = ('file',)

class FileUploadSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserUploads
        # fields  = '__all__'
        exclude = ('user',)

class ProfileUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields  = '__all__'
        fields = ('User_profile',)
    
    def update(self, instance, validated_data):
        instance.User_profile = validated_data.get('User_profile', instance.User_profile)
        instance.save()
        return instance


class Get_Address_Serializers(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(lookup_field='pk',read_only=True,view_name='address-detail')
    class Meta:
        model=Address
        # exclude =('updated_at','created_at','user')
        fields =('url','name','first_address','city','contact_no')

    def update(self, instance, validated_data):
        # Update specific fields based on validated_data
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def __init__(self, *args, **kwargs):
        # Call the parent class' __init__ method
        super().__init__(*args, **kwargs)

        # Access the request object from the serializer's context
        request = self.context.get('request')

        # Check if the request method is 'PUT' (update request)
        if request and request.method == 'PUT':
            # Remove the 'url' field from the serializer's fields
            self.fields.pop('url', None)












































