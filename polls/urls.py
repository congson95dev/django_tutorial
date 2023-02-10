from django.urls import path

from . import views


# set app_name so when we call {% url %} in templates, it will select by app_name
app_name = 'polls'
# setup url, and connect them to function in views.py
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
