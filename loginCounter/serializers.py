from django.forms import widgets
from rest_framework import serializers
from loginCounter.models import User

# class UserSerializer(serializers.Serializer):
# 	user = serializers.CharField(max_length=128)
# 	password = serializers.CharField(max_length=128)
# 	count = serializers.IntegerField()

# 	def restore_objects(self, attrs, instance=None):
# 		if instance:
# 			instance.user = attrs.get('user', instance.user)
# 			instance.password = attrs.get('password', instance.password)
# 			instance.count = attrs.get('count', instance.count)
# 			return instance
# 		return User(**attrs)

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('user', 'password')