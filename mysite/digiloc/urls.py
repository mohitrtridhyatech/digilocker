from django.urls import path, include
from .views import  userAPIView,LogoutView,RegistrationView, home_page, UserLoginView, FileuploadView, metadataViewSet , AuthViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('metadata',metadataViewSet,basename='metadata')
router.register('get',AuthViewSet, basename='get')


urlpatterns = [
    path('home',home_page, name='home'),
    path('users', userAPIView.as_view(), name='users'),
    path('login',UserLoginView.as_view(), name='login'),
    path('logout',LogoutView.as_view(), name='logout'),
    path('register',RegistrationView.as_view(), name='register'),

    path('fileup',FileuploadView.as_view(), name='fileup'),
    path('editdata/<int:id>',FileuploadView.as_view(), name='editdata'),

    # path('generic/metadata/<str:uu_id>/', GenericAPIView.as_view()),
    # path('generic/metadata/', GenericAPIView.as_view()),

    path('viewset/', include(router.urls)),
    path('user/', include(router.urls)),
    # path('viewset/<str:uu_id>/', include(router.urls)),
]