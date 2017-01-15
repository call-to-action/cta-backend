
from .models import *
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import viewsets, generics
from cta.permissions import IsAdminOrIsSelf
from rest_framework.decorators import detail_route

from .serializers import  *


class CtaUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CtaUser.objects.all().order_by('-created_at')
    serializer_class = CtaUserPublicSerializer


    @detail_route(methods=['post'])#, permission_classes=[IsAdminOrIsSelf])
    def set_password(self, request, pk=None):
        #send email with sendgrid or something 
        pass

class CallToActionViewSet(viewsets.ModelViewSet):
    queryset = CallToAction.objects.all().order_by('-created_at')
    serializer_class = CallToActionSerializer


class UserCallToActionViewSet(viewsets.ModelViewSet):
    queryset = UserCallToAction.objects.all().order_by('-created_at')
    serializer_class = UserCallToActionSerializer

    @detail_route(methods=['post'])#, permission_classes=[IsAdminOrIsSelf])
    def accept_cta(self, request, pk=None):
        user_cta,c = UserCallToAction.objects.get_or_create(cta__id=pk,user=request.user)
        user_cta.status = 1
        user_cta.save()
        

    @detail_route(methods=['post'])#, permission_classes=[IsAdminOrIsSelf])
    def reject_cta(self, request, pk=None):
        user_cta,c = UserCallToAction.objects.get_or_create(cta__id=pk,user=request.user)
        user_cta.status = 0
        user_cta.save()

    @detail_route(methods=['post'])#, permission_classes=[IsAdminOrIsSelf])        
    def bookmark_cta(self, request, pk=None):
        user_cta,c = UserCallToAction.objects.get_or_create(cta__id=pk,user=request.user)
        user_cta.status = 2
        user_cta.save()


class UserSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = UserSubscription.objects.all().order_by('-created_at')
    serializer_class = UserSubscriptionSerializer


class GetUserCtas(generics.ListCreateAPIView):
    queryset = CallToAction.objects.all()
    serializer_class = CallToActionSerializer

    def list(self, request):
        user_id = self.kwargs['user_id']
        queryset = self.get_queryset()
        queryset = queryset.filter(created_by__id=user_id)
        serializer = CallToActionSerializer(queryset, many=True)
        return Response(serializer.data)

class GetBookmarkedCtas(generics.ListCreateAPIView):
    queryset = UserCallToAction.objects.all()
    serializer_class = UserCallToActionSerializer

    def list(self, request):
        #user_id = self.kwargs['user_id'] should this be public
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        queryset = queryset.filter(user=self.request.user,status=2) #bogus status
        serializer = CallToActionSerializer(queryset, many=True)
        return Response(serializer.data)


class GetApprovedCtas(generics.ListCreateAPIView):
    queryset = UserCallToAction.objects.all()
    serializer_class = UserCallToActionSerializer

    def list(self, request):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(CtaUser,id=user_id)
        if user == self.request.user or user.is_activity_public:
        # Note the use of `get_queryset()` instead of `self.queryset`
            queryset = self.get_queryset()
            queryset = queryset.filter(user=self.request.user,status=1) #bogus status
            serializer = CallToActionSerializer(queryset, many=True)
        else:
            return Http404 
        return Response(serializer.data)

class GetDeclinedCtas(generics.ListCreateAPIView):
    queryset = UserCallToAction.objects.all()
    serializer_class = UserCallToActionSerializer

    def list(self, request):
        user_id = self.kwargs['user_id']
        if user_id != self.request.user.id:
            raise Http404
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        queryset = queryset.filter(user__id=user_id)
        serializer = CallToActionSerializer(queryset, many=True)
        return Response(serializer.data)

class GetCreatedCtas(generics.ListCreateAPIView):
    queryset = CallToAction.objects.all()
    serializer_class = CallToActionSerializer

    def list(self, request):
        user_id = self.kwargs['user_id']
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        queryset = queryset.filter(created_by__id=user_id) #NOT IN CAllToActionTable
        serializer = CallToActionSerializer(queryset, many=True)
        return Response(serializer.data)


class GetAvailableCtas(generics.ListCreateAPIView):
    queryset = CallToAction.objects.all()
    serializer_class = CallToActionSerializer

    def list(self, request):
        user_id = self.kwargs['user_id']
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        #filter by UserCallToAction
        serializer = CallToActionSerializer(queryset, many=True)
        return Response(serializer.data)

class SearchAvailableCtas(generics.ListCreateAPIView):
    queryset = CallToAction.objects.all()
    serializer_class = CallToActionSerializer

    def list(self, request):
        term = self.kwargs['term']
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        queryset = queryset.filter(tag__contains=term) #NOT IN CAllToActionTable
        serializer = CallToActionSerializer(queryset, many=True)
        return Response(serializer.data)


class GetLoggedInUser(generics.ListCreateAPIView):
    queryset = CtaUser.objects.all()
    serializer_class = CtaUserPrivateSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        queryset = queryset.filter(user=self.request.user)
        serializer = CtaUserSerializer(queryset, many=True)
        return Response(serializer.data)


class GetSubscribers(generics.ListCreateAPIView):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer

    def list(self, request):
        user_id = self.kwargs['user_id']
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        queryset = queryset.filter(subscription__id=user_id)
        serializer = UserSubscriptionSerializer(queryset, many=True)
        return Response(serializer.data)


class GetSubscriptions(generics.ListCreateAPIView):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer

    def list(self, request):
        user_id = self.kwargs['user_id']
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        queryset = queryset.filter(subscriber__id=user_id)
        serializer = UserSubscriptionSerializer(queryset, many=True)
        return Response(serializer.data)
