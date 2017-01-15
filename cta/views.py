from .models import *
from rest_framework import viewsets
from .serializers import  *


class CtaUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CtaUser.objects.all().order_by('-date_joined')
    serializer_class = CtaUserPublicSerializer


class CallToActionViewSet(viewsets.ModelViewSet):
    queryset = CtaUser.objects.all().order_by('-date_joined')
    serializer_class = CallToActionSerializer

class UserCallToActionViewSet(viewsets.ModelViewSet):
    queryset = UserCallToAction.objects.all().order_by('-date_joined')
    serializer_class = UserCallToActionSerializer


class UserSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = UserSubscription.objects.all().order_by('-date_joined')
    serializer_class = UserSubscriptionSerializer

