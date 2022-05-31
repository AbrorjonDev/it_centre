from re import L
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ("id", "username", "first_name", "last_name", "password", "is_admin", "is_director")

        extra_kwargs = {
            "password":{"write_only":True},
        }

    def create(self, attrs):
        if self.context["request"].user.is_superuser:
            user = User.objects.create(**attrs, is_admin=False)
        else:
            user = User(**attrs, is_admin=True, is_director=False)
        user.set_password(attrs.get("password"))
        user.save()
        return user
    
    def update(self, instance, attrs):
        instance.username = attrs.get("username", instance.username)
        instance.is_admin = attrs.get("is_admin", instance.is_admin)
        if self.context["request"].user.is_superuser:
            instance.is_director = attrs.get("is_director", instance.is_director)
        if "password" in attrs.keys():
            instance.set_password(attrs["password"])
        instance.save()
        return instance




class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True, style={"input_type":"password", "placeholder":"Old Password"})
    new_password1 = serializers.CharField(write_only=True, required=True, style={"input_type":"password", "placeholder":"New Password"})
    new_password2 = serializers.CharField(write_only=True, required=True, style={"input_type":"password", "placeholder":"New Password Confirmation"})


    def validate(self, data):
        if not self.context["request"].user.check_password(data["old_password"]):
            raise serializers.ValidationError("Old password doesn't match your password.", code=403)
        if data["new_password1"] != data["new_password2"]:
            raise serializers.ValidationError("Password confirmation doesn't equal.",code=400)
        return data
    
    def save(self):
        data = self.validated_data
        user = self.context["request"].user
        user.set_password(data["new_password1"])
        user.save()
        user.auth_token.delete()
        return user

