from django.urls import path
from . import views
app_name='polls'
urlpatterns=[
    path('',views.IndexView.as_view(),name='index'),
    path('<int:pk>',views.DetailView.as_view(),name='detail'),
    path('<int:pk>/results',views.ResultsView.as_view(),name='results'),
    path('<int:question_id>/vote',views.vote,name='vote')
]

#question_id에서 pk로 변경
#question_id새로운 변수 사용하려면 상속이아니라 인수를 받아와야함
