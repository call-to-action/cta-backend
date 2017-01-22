from django.conf.urls import url,include
from rest_framework import routers
from django.contrib import admin
from cta import views

router = routers.DefaultRouter()
router.register(r'users', views.CtaUserViewSet)
router.register(r'cta', views.CallToActionViewSet)
router.register(r'subscriptions', views.UserSubscriptionViewSet)
router.register(r'usercta', views.UserCallToActionViewSet)
import views


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [

    url(r'^$', views.signup,name="signup"),
    url(r'^$', views.signup,name="results"),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^/api/users/ctas/:user_id/$', views.GetUserCtas.as_view()),
    url(r'^/api/ctas/search/:term/$', views.SearchAvailableCtas.as_view()),
    url(r'^/api/users/me/$', views.GetLoggedInUser.as_view()),
    url(r'^/api/users/subscribers/:user_id/$', views.GetSubscribers.as_view()),
    url(r'^/api/users/subscriptions/:user_id/$', views.GetSubscriptions.as_view()),
    url(r'^/api/ctas/approved/:user_id/$', views.GetApprovedCtas.as_view()),
    url(r'^/api/ctas/declined/:user_id/$', views.GetDeclinedCtas.as_view()),
    url(r'^/api/ctas/bookmarked/:user_id/$', views.GetBookmarkedCtas.as_view()),
    url(r'^/api/ctas/available/:user_id/$', views.GetAvailableCtas.as_view()),
    url(r'^/api/ctas/created/:user_id/$', views.GetCreatedCtas.as_view()),

    url(r'^', include(router.urls)),
]
