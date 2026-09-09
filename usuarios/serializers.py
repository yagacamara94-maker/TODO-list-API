from rest_framework.serializers import ModelSerializer,CharField,EmailField
from .models import CustomUser
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions


class create_user_serializer(ModelSerializer):
    confirm_password = CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id','username','email','password','confirm_password']
        extra_kwargs = {
             'password':{'write_only':True}
        }

    def validate_username(self,username):
            username = username.strip()
            if len(username) < 3:
                raise ValidationError("O nome de usuário não pode conter menos de três caracteres!")
            return username
    def validate(self,attrs):
        try:
            validate_password(password=attrs['password'], user=self.instance)
        except exceptions.ValidationError as e:
            raise ValidationError(e.messages)
        if attrs['password'] != attrs['confirm_password']:
            raise ValidationError("As senhas não coicidem!")

        return attrs
             
             

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
        username=validated_data['username'],
        email=validated_data['email'],
        password=validated_data['password']
        )

        return user
    
