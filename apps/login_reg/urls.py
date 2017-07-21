from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^main', index, name="index"),
    url(r'^authenticate$', authenticate, name="authenticate"),
    url(r'^quotes$', quote_home, name="quote_home"),
    url(r'^logout$', logout, name="logout"),

    url(r'^user/(?P<user_id>\d+)$', user_info, name="user_info"),
    
    url(r'^quotes/add$', quote_add, name="quote_add"),
    

    url(r'^favorite/delete/(?P<quote_id>\d+)$', favorite_delete, name="favorite_delete"),
    url(r'^favorite/add/(?P<quote_id>\d+)$', favorite_add, name="favorite_add"),
    ]

