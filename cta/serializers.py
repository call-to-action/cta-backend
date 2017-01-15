from rest_framework import serializers
from .models import *

class CtaUserPrivateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CtaUser

class CtaUserPublicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CtaUser
        fields = ('id','name','is_verified','is_corporation')

class CallToActionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CallToAction
        fields = ('id','created_by','title','description','action_item','phone','created_at','updated_at') #tags

class UserCallToActionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserCallToAction
        fields = ('id','user', 'cta', 'status', 'created_at')

class UserSubscriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserSubscription
        fields = ('subscriber', 'subscription', 'status', 'created_at')
