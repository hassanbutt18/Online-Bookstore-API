from users.models import CustomUser
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    role = serializers.CharField(required=True)

    def validate(self,attrs):
        role = attrs.get('role',None)
        email = attrs.get('email',None)
        roles_list = ['author','buyer','admin']
        if role not in roles_list:
            raise ValidationError({"msg":f"Enter the valid role"})
        if role is not None and email is not None:
            user = CustomUser.objects.filter(email=email , role=role)
            if user.exists():
                raise ValidationError({"msg": "User already exists with same role you can login"})
            user = CustomUser.objects.filter(email=email)
            if user.exists():
                raise ValidationError({"msg": "User already exists"})

        return attrs

    class Meta:
        model = CustomUser
        fields = ['email', 'password','role']



    def create(self, validated_data):
        user = CustomUser.objects.create_user(
                                        email=validated_data.get('email'),password=validated_data.get('password'),
                                        role=validated_data.get('role',None)
                                        )
        return user
