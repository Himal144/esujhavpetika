from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout 
from .forms import signupform
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import signupform , organization_register_form
from . models import Organization
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .send_email import EmailThread
from django.template.loader import render_to_string
from django.db.models.functions import TruncWeek
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
 

from . models import Organization

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Organization
from django.contrib.auth.decorators import login_required
from .models import *
from user.models import Sender
 

def organization_detail(request, id):
    organization = get_object_or_404(Organization, id=id)
   
    context = {
        'organization': organization,
        'organization_url': f"http://127.0.0.1:8000/organization/{organization.id}/"
    }
    return render(request, 'organization/organization.html', context)

def baseapp (request):
    return render(request,'organization/home.html')



def login_form(request):
    if request.method == 'POST':
        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/organization/dashboard")
             
    else:
        fm = AuthenticationForm()
    
    context = {"loginform": fm}
    return render(request, "organization/login.html", context)

def signup_form(request):
    if request.method == "POST":
        fm = signupform(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request, 'Account Created successfully')
            fm = AuthenticationForm()
            context = {"loginform": fm}
            return render(request, "organization/login.html", context)
        else:
            return render(request, 'organization/signup.html', {'signupform': fm})
    else:
        fm = signupform()
        return render(request, 'organization/signup.html', {'signupform': fm})
@login_required
def user_logout(request):
    logout(request)
    messages.warning(request,"Log out succefully")
    return HttpResponseRedirect('/')

@login_required
def feedback(request):
    user=get_object_or_404(User, id=request.user.id)
    try:
        organization=get_object_or_404(Organization,user=user)
    except organization.DoesNotExist:
        organization=None    
    if (organization):
            feedbacks_by_topic = Feedback.objects.filter(organization_id=organization) \
                                             .values('topic_id') \
                                             .annotate(feedback_count=Count('id')) \
                                             .order_by('-feedback_count')
            if feedbacks_by_topic.exists():
                feedback_context={}
                for topic_feedback in feedbacks_by_topic:
                    topic_id = topic_feedback['topic_id']
                    topic_name = Topic.objects.get(id=topic_id).topic
                    feedbacks = Feedback.objects.filter(organization_id=organization, topic_id=topic_id)
                    feedback_list = []
                    for feedback in feedbacks:
                        similarity_count=Similarity.objects.filter(feedback_id=feedback.id).count()
                        feedback_list.append({
                    'id':feedback.id,        
                    'feedback': feedback.feedback,
                    'date': feedback.date,
                    'sender': feedback.sender_id,
                    'status': feedback.status,
                    'similarity_count':similarity_count
                    })

                    feedback_context[topic_name] = feedback_list
                return render(request,'organization/feedback.html',{"feedback_context":feedback_context})
            return render(request,'organization/feedback.html',{"feedback_context":{}})         
                # Retrieve the feedbacks for this specific topic
                
@csrf_exempt      
def handle_feedback_action(request):
    if request.method=='POST':
        
        try:
            data = json.loads(request.body)
            feedback_id = data.get('feedback_id')
            dropdown_clicked_id = int(data.get('dropdown_clicked_id'))

            response_message = data.get('response')
            #Code to handle the solved of the problem
            if dropdown_clicked_id == 0:
                feedback_obj=Feedback.objects.get(id=feedback_id)
                feedback_obj.status=True
                feedback_obj.save()
                #Code to send the email

                sender_id_list=Similarity.objects.filter(feedback_id=feedback_id).values('sender_id')
                recipient_list=[]
                for sender in sender_id_list:
                    sender_obj=Sender.objects.get(id=sender["sender_id"])
                    sender_email=sender_obj.email
                    recipient_list.append(sender_email)
                    sender_name=sender_obj.name
                    context={
                          'name':sender_name,
                          'feedback':feedback_obj.feedback
                    }

                    html_content = render_to_string('organization\mail.html', context)
                    subject = "Suggestion"
                   
                    
                #send_email_to_client function is in the utils.py file
                    email_thread = EmailThread(subject, html_content, recipient_list)
                    email_thread.start()


            #Code to handle the unable to solve 
            elif dropdown_clicked_id == 1:
                feedback_obj=Feedback.objects.get(id=feedback_id)
                feedback_obj.status=False
                feedback_obj.save()
                #code to send the email


            #Cod to handle the forward the feedback to the parent
            elif dropdown_clicked_id == 2:
                forward=Forward()
                forward.feedback_id=Feedback.objects.get(id=feedback_id)
                forward.organization_id=Organization.objects.get(user=request.user)
                forward.save()
                
            return JsonResponse({'status': 'success', 'message': 'Response send successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
 

def organization_register(request):
    try:
        organization = Organization.objects.get(user=request.user)
        form = organization_register_form(request.POST, request.FILES, instance=organization)
    except Organization.DoesNotExist:
        form = organization_register_form(request.POST, request.FILES)
    
    if request.method == 'POST':
        if form.is_valid():
            extra_data = request.POST.get('type')
            organization = form.save(commit=False)
            organization.user = request.user
            organization.save()

            if extra_data =="single":
                messages.success(request,"Organizartion register successfully")
                redirect_url = '/'
            else:
                messages.success(request,"Organization register successfully.Please add info of each department.")
                redirect_url = "/organization/register/multi-department/"    

            return JsonResponse({'redirect_url': redirect_url})
    else:
          form = organization_register_form()    
    
    return render(request, 'organization/register.html', {'organization_register_form': form})

#code for the multi department register form
@csrf_exempt 
def multi_department(request):
  
    if request.method == 'POST':
        department_data = []
        existing_users = []

        for key in request.POST:
            if key.startswith('name_'):
                index = key.split('_')[1]
                department = {
                    'index': index,
                    'name': request.POST[f'name_{index}'],
                    'email': request.POST[f'email_{index}'],
                    'authenticated_sender': request.POST.get(f'authenticated_sender_{index}') == 'true'
                }
                department_data.append(department)

        user_credentials = []
        existing_email = []

        # First pass: Check for existing users
        for data in department_data:
            username = data["email"]
            user = User.objects.filter(username=username).first()
            if user is not None:
                existing_email.append({
                    'index': data['index'],
                    'email': username
                })

        # If there are existing users, return the information
        if existing_email:
            return JsonResponse({
                "existing_user": True,
                "existing_email": existing_email
            }, status=400)

        # Second pass: Create new users and organizations
        for data in department_data:
            username = data["email"]
            password = get_random_string(8)  # Generate a random 8-character password
            user_created = False

            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=username, password=password)
                user.save()
                user_created = True
                user_credentials.append({
                    'email': username,
                    'password': password,
                    'status': 'User created successfully'
                })

                # Creating the organization for each user
                name = data["name"]
                parent = request.user
                parent_organization = Organization.objects.get(user=parent)
                logo = parent_organization.logo
                authenticated_sender = data["authenticated_sender"]
                organization = Organization.objects.create(
                    user=user, 
                    name=name, 
                    logo=logo, 
                    parent_id=parent.id, 
                    authenticated_sender=authenticated_sender
                )
                organization.save()
            else:
                user_credentials.append({
                    'email': username,
                    'status': 'User already exists',
                    'index': data['index']
                })

        return JsonResponse({
            'message': 'Departments registered successfully',
            'users': user_credentials
        }, status=200)
    
    return render(request, 'organization/multi_department.html')

 

# Code for the dashboard 
@login_required
def dashboard(request):
    user_obj=request.user
    organization_obj=Organization.objects.get(user=user_obj)
    organization_child_obj=Organization.objects.filter(parent_id=organization_obj.id)
    if organization_child_obj.exists():
        #code for the parent organization
        pass
    else:
        #code for the child organization
        latest_suggestion_list=[]
        frequent_suggestions=[]
        logo_url=organization_obj.logo
        feedback_obj=Feedback.objects.filter(organization_id=organization_obj)
        problem_count=feedback_obj.count
        solved_count=feedback_obj.filter(status=True).count()
        latest_suggestion_obj=feedback_obj.order_by("-date")[:3]
        for latest_suggestion in latest_suggestion_obj:
            sender=latest_suggestion.sender_id
            suggestion={
                "user":sender.name,
                "time":latest_suggestion.date,
                "feedback":latest_suggestion.feedback
            }
            latest_suggestion_list.append(suggestion)
        feedbacks_by_topic = feedback_obj \
                                             .values('topic_id') \
                                             .annotate(feedback_count=Count('id')) \
                                             .order_by('-feedback_count')[:3]    
        for feedback in feedbacks_by_topic:
            topic_obj=Topic.objects.get(id=feedback['topic_id'])
            topic=topic_obj.topic
            feedback_obj=Feedback.objects.filter(topic_id=topic_obj,status=None)
            feedback_count_by_topic=feedback_obj.count()
            latest_time_obj=feedback_obj.order_by("-date").first()
            suggestion={
                'topic':topic,
                "count":feedback_count_by_topic,
                "latest_time":latest_time_obj.date
            }
            frequent_suggestions.append(suggestion)
        feedbacks_by_week = feedback_obj.annotate(week=TruncWeek('date')).values('week').annotate(count=Count('id')).order_by('week') 
        today = timezone.now()
        start_of_week = today - timedelta(days=today.weekday())
        
        weeks = [start_of_week - timedelta(weeks=i) for i in range(4)]
        week_labels = [f"Week {i+1}" for i in range(4)]
        week_counts = [
            feedback_obj.filter(date__gte=weeks[i], date__lt=weeks[i] + timedelta(weeks=1)).count()
            for i in range(4)
        ]
        
        statistics = {
            'labels': week_labels,
            'values': week_counts,
        }  
       
    # Dummy data for the dashboard
    context = {
        'logo_url': 'path_to_logo_image',  # Update with the actual path or URL to the logo image
        'problems_count': problem_count,
        'solved_count': solved_count,
        'latest_suggestion':latest_suggestion_list,
        'frequent_suggestions': frequent_suggestions,
        'statistics': statistics
    }
    return render(request, 'organization/dashboard.html', context)

def insights(request):
  
    # Dummy data for demonstration
    statistics = {
        'labels': ['January', 'February', 'March', 'April', 'May', 'June'],
        'values': [12, 19, 3, 5, 2, 3]
    }
    
    double_statistics = {
        'labels': ['January', 'February', 'March', 'April', 'May', 'June'],
        'values_a': [12, 19, 3, 5, 2, 3],
        'values_b': [8, 11, 5, 7, 1, 4]
    }

    context = {
        'statistics': statistics,
        'double_statistics': double_statistics
    }

    return render(request, 'organization/insights.html', context)
