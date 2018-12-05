from django.urls import path, include, re_path
from .views import (
    SignOut,
    Sign_In,
    SignUp,
    UserDetail,
    UserEdit,
    ChangePass
)


app_name = 'accounting'

urlpatterns = [
    path('signout/', SignOut.as_view(), name='signout'),
    path('signin/', Sign_In.as_view(), name='signin'),
    path('signup/', SignUp.as_view(), name = 'signup'),
    re_path(r'^(?P<username>[\w.@+-]+)/edit$', UserEdit.as_view(), name='UserEdit'),
    re_path(r'^(?P<username>[\w.@+-]+)/changepass$',ChangePass.as_view(), name='passchange'),
    re_path(r'^(?P<username>[\w.@+-]+)/$', UserDetail.as_view(), name='UserDetail')
]
