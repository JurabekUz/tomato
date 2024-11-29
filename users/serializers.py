from rest_framework.serializers import ModelSerializer


from .models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'phone', 'first_name', 'last_name', 'father_name', 'email', 'password', 'language')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)



