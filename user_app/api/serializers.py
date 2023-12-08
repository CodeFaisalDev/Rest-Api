from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]
        email = self.validated_data["email"]
        username = self.validated_data["username"]

        if password != password2:
            raise serializers.ValidationError('Both Password Should Be Same')

        user_queryset = User.objects.filter(email=email)
        if user_queryset.exists():
            raise serializers.ValidationError('User with this email already exists')

        # Create a new user instance and set the password
        account = User(username=username, email=email)
        account.set_password(password)
        account.save()

        return account
