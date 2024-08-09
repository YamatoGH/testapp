from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-test/', views.create_test, name='create_test'),
    path('test/<int:pk>/', views.test_detail, name='test_detail'),
    path('print-test/<int:pk>/<int:start_index>/<int:end_index>/<str:shuffle>/', views.print_test, name='print_test'),
    path('print-test-with-answers/<int:pk>/<int:start_index>/<int:end_index>/<str:shuffle>/', views.print_test_with_answers, name='print_test_with_answers'),
    path('add-student/', views.add_student, name='add_student'),
    path('students/', views.student_list, name='student_list'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('group-tests/<int:pk>/', views.group_tests, name='group_tests'),
]
