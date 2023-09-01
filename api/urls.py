from django.urls import path,include
from api import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'address', views.Get_Address,basename="address")
urlpatterns = [
    path(r'user/', include(router.urls),name="index"),
    path('',views.UserHome.as_view(),name="home"),
    path(r'login/',views.user_login_view,name="login"),
    path(r'register/',views.user_register_view,name="register"),
    path(r'fileupload/',views.upload_file,name="fileupload"),
    path(r'byusers/',views.byusers,name="byusers"),
    path(r'byfiles/',views.byfiles,name="byfiles"),
    path(r'profile/',views.profile,name="profile"),
    path(r'deshboard/',views.deshboard,name="admin"),
    path(r'admin_user/',views.admin_user,name="admin-login"),
    path(r'profile_user/',views.profile_user,name="profile_user"),
    
]
