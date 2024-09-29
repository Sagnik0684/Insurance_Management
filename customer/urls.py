from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from .views import chatbot_response

urlpatterns = [
    path('customerclick', views.customerclick_view, name='customerclick'),
    path('customersignup/', views.customer_signup_view, name='customersignup'),
    path('account-creation-success/', views.account_creation_success_view, name='account_creation_success'),
    path('customerlogin', LoginView.as_view(template_name='insurance/adminlogin.html'), name='customerlogin'),
    path('customer-dashboard', views.customer_dashboard_view, name='customer-dashboard'),
    path('apply-policy', views.apply_policy_view,name='apply-policy'),
    path('apply/<int:pk>', views.apply_view,name='apply'),

    path('create_razorpay_order/<int:pk>/', views.create_razorpay_order, name='create_razorpay_order'),
    path('razorpay_payment_success/', views.razorpay_payment_success, name='razorpay_payment_success'),

    path('history', views.history_view,name='history'),

    path('ask-question', views.ask_question_view,name='ask-question'),
    path('question-history', views.question_history_view,name='question-history'),

    path('premium-interest-calculator/', views.premium_interest_calculator_view, name='premium-interest-calculator'),
    path('policies/', views.customer_policies_view, name='customer_policies'),
    path('policies/add/', views.add_policy_view, name='add_policy'),
    path('policies/delete/<int:policy_id>/', views.delete_policy_view, name='delete_policy'),

    path('chatbot/', chatbot_response, name='chatbot_response'),
]