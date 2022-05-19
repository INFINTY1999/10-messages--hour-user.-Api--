from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class userSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type' : 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['id','username','email','password','password2']
        extra_kwargs = {
            'password' : {'write_only':  True},
            'id' : {'read_only':  True},
        }
        
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'error':'P1 and P2 should be same'})
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error':'this email already exits!'})

        account = User(email=self.validated_data['email'],username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        return account
    

class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = message
        fields = ['id','message','created_at','updated_at','created_by']
        extra_kwargs = {
            'id' : {'read_only':  True},
            'created_at' : {'read_only':  True},
            'updated_at' : {'read_only':  True},
            'created_by' : {'read_only':  True},
        }
        
class MessSerializer(serializers.ModelSerializer):
    created_by = userSerializer(many=False)
    class Meta:
        model = message
        fields = ['id','message','created_at','updated_at','created_by']
