from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('test/<int:test_id>/', views.test_detail, name='test_detail'),
    path('print-test/<int:test_id>/<int:start_index>/<int:end_index>/<str:shuffle>/', views.print_test, name='print_test'),
    path('print-test-with-answers/<int:test_id>/<int:start_index>/<int:end_index>/<str:shuffle>/', views.print_test_with_answers, name='print_test_with_answers'),
    path('create-test/', views.create_test, name='create_test'),
    path('group-tests/<int:group_id>/', views.group_tests, name='group_tests'),
    path('all-tests/', views.all_tests, name='all_tests'),
]

