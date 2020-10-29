from django.urls import path
from . import views

app_name='accounts'

urlpatterns = [
    path('signup/<role>',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    #path('<role>/<int:id>/',views.profile,name='profile'),
    path('profile/<role>',views.profile,name='profile'),
]