from django.urls import path
from . import views


# setup url, and connect them to function in views.py
urlpatterns = [
    path('learn_get_query', views.learn_get_query, name='learn_get_query'),
    path('learn_create_update_delete_query', views.learn_create_update_delete_query, name='learn_create_update_delete_query'),
    path('show_product_ordered', views.show_product_ordered, name='show_product_ordered'),
    path('get_last_5_ordered', views.get_last_5_ordered, name='get_last_5_ordered'),
]
