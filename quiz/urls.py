from django.urls import path
from . import views

app_name = 'quiz'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('test/<uuid:test_id>', views.TestDetailView.as_view(), name='test_detail'),
    path('test/page/<uuid:test_id>/', views.TestPageView.as_view(), name='test_page'),
    path('results/', views.ResultsListView.as_view(), name='results'),
    path('result/detail/<uuid:attempt_id>/', views.ResultDetailView.as_view(), name='result_detail')
]