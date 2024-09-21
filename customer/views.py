from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from insurance import models as CMODEL
from insurance import forms as CFORM
from django.contrib.auth.models import User
from django.urls import reverse
from .models import CustomerPolicy
from .forms import CustomerPolicyForm

def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'customer/customerclick.html')

def customer_signup_view(request):
    userForm = forms.CustomerUserForm()
    customerForm = forms.CustomerForm()
    mydict = {'userForm': userForm, 'customerForm': customerForm}

    if request.method == 'POST':
        print("POST request received")  # Debugging point 1
        userForm = forms.CustomerUserForm(request.POST)
        customerForm = forms.CustomerForm(request.POST, request.FILES)
        
        # Ensure that both forms are valid
        if userForm.is_valid() and customerForm.is_valid():
            print("Forms are valid")  # Debugging point 2

            # Save the user and customer form
            user = userForm.save(commit=False)
            user.set_password(user.password)  # Encrypt password
            user.save()

            customer = customerForm.save(commit=False)
            customer.user = user
            customer.save()

            # Add user to the 'CUSTOMER' group
            my_customer_group, created = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group.user_set.add(user)

            print("Account created. Redirecting to success page.")  # Debugging point 3

            # Redirect to account creation success page
            return redirect('account_creation_success')
        
        else:
            # If form is invalid, print errors (for debugging)
            print("User form errors: ", userForm.errors)
            print("Customer form errors: ", customerForm.errors)
    
    print("Rendering signup page")  # Debugging point 4
    # Render the signup page with the forms
    return render(request, 'customer/customersignup.html', context=mydict)
def account_creation_success_view(request):
    return render(request, 'customer/account_creation_success.html')

def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()

@login_required(login_url='customerlogin')
def customer_dashboard_view(request):
    # Get the customer instance for the logged-in user
    customer = models.Customer.objects.get(user_id=request.user.id)

    # Fetch available policies
    available_policy_count = CMODEL.Policy.objects.all().count()

    # Fetch applied policies for the current customer
    applied_policy_count = CMODEL.PolicyRecord.objects.filter(customer=customer).count()

    # Fetch total categories
    total_category_count = CMODEL.Category.objects.all().count()

    # Fetch total questions asked by the current customer
    total_question_count = CMODEL.Question.objects.filter(customer=customer).count()

    # Fetch cheapest policy for each category
    categories = CMODEL.Category.objects.all()
    recommendations = []

    for category in categories:
        cheapest_policy = CMODEL.Policy.objects.filter(category=category).order_by('premium').first()
        if cheapest_policy:
            recommendations.append(cheapest_policy)

    # Creating a context dictionary to pass to the template
    dict = {
        'customer': customer,
        'available_policy': available_policy_count,
        'applied_policy': applied_policy_count,
        'total_category': total_category_count,
        'total_question': total_question_count,
        'recommendations': recommendations,  # Cheapest policy recommendations
    }

    # Render the dashboard template with the context
    return render(request, 'customer/customer_dashboard.html', context=dict)
def apply_policy_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    policies = CMODEL.Policy.objects.all()
    return render(request,'customer/apply_policy.html',{'policies':policies,'customer':customer})

def apply_view(request,pk):
    customer = models.Customer.objects.get(user_id=request.user.id)
    policy = CMODEL.Policy.objects.get(id=pk)
    policyrecord = CMODEL.PolicyRecord()
    policyrecord.Policy = policy
    policyrecord.customer = customer
    policyrecord.save()
    return redirect('history')

def history_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    policies = CMODEL.PolicyRecord.objects.all().filter(customer=customer)
    return render(request,'customer/history.html',{'policies':policies,'customer':customer})

def ask_question_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    questionForm=CFORM.QuestionForm() 
    
    if request.method=='POST':
        questionForm=CFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            
            question = questionForm.save(commit=False)
            question.customer=customer
            question.save()
            return redirect('question-history')
    return render(request,'customer/ask_question.html',{'questionForm':questionForm,'customer':customer})

def question_history_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    questions = CMODEL.Question.objects.all().filter(customer=customer)
    return render(request,'customer/question_history.html',{'questions':questions,'customer':customer})


def premium_interest_calculator_view(request):
    if request.method == 'POST':
        # Fetch data from the form submission
        principal = float(request.POST.get('principal', 0))
        rate = float(request.POST.get('rate', 0))
        time = float(request.POST.get('time', 0))
        
        # Calculate simple interest
        interest = (principal * rate * time) / 100
        total_amount = principal + interest
        
        # Prepare context for the template
        context = {
            'principal': principal,
            'rate': rate,
            'time': time,
            'interest': interest,
            'total_amount': total_amount,
        }
        
        # Render the template with context
        return render(request, 'customer/premium_interest_calculator.html', context)
    
    # Handle GET requests
    return render(request, 'customer/premium_interest_calculator.html')


@login_required
def customer_policies_view(request):
    policies = CustomerPolicy.objects.filter(user=request.user)
    return render(request, 'customer/customer_policies.html', {'policies': policies})

@login_required
def add_policy_view(request):
    if request.method == 'POST':
        form = CustomerPolicyForm(request.POST)
        if form.is_valid():
            policy = form.save(commit=False)
            policy.user = request.user  # Assign the current logged-in user to the policy
            policy.save()
            return redirect('customer_policies')
    else:
        form = CustomerPolicyForm()
    return render(request, 'customer/add_policy.html', {'form': form})

@login_required
def delete_policy_view(request, policy_id):
    policy = CustomerPolicy.objects.get(id=policy_id, user=request.user)
    if request.method == 'POST':
        policy.delete()
        return redirect('customer_policies')
    return render(request, 'customer/delete_policy.html', {'policy': policy})


