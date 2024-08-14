from django.shortcuts import render 
from django.contrib.auth.models import User
from . models import Organization
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from user.models import Sender
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout 
from .forms import signupform
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import signupform , organization_register_form
from . models import Organization
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .send_email import EmailThread
from django.template.loader import render_to_string
from django.db.models.functions import TruncWeek
from django.db.models import Count 
from django.utils import timezone
from datetime import timedelta
import json
import re,os
from django.db.models import Q
from esujhavpetika.context_processor import get_suggestion_box_status
from django.urls import reverse
from .forms import MyPasswordChangeForm,OrganizationLogoForm
 


 
#Code for generating the QR code of the organization
@login_required 
def organization_detail(request):

#code for making the organization name url compatible
    def slugify(text):
        # Convert to lowercase
        text = text.lower()
        # Replace spaces with hyphens
        text = re.sub(r'\s+', '-', text)
        # Remove special characters
        text = re.sub(r'[^a-z0-9\-]', '', text)
        return text

    child_organization_qs=Organization.objects.filter(parent_id=request.user.id) 
    parent_organization=Organization.objects.filter(user=request.user).first()
    parent_user_obj=User.objects.get(id=parent_organization.user.id)
    parent_name=parent_organization.name
    parent_slug_name=slugify(parent_name)
        #code for the parent organization
    if child_organization_qs.exists():
        
        child_organizations=[]
        for child_organization_obj in child_organization_qs:
            user_obj=User.objects.get(id=child_organization_obj.user.id)
            name= child_organization_obj.name
            slug_name=slugify(name)
            child_organizations.append({
                'child_logo_url':child_organization_obj.logo.url,
                'url': f"http://127.0.0.1:8000/suggestion/{slug_name}/{child_organization_obj.id}/",
                'username':user_obj.username,
                'joined_date':user_obj.date_joined.date().isoformat(),
                'name':name
            })
        
        context = {
            'child_organization': child_organizations,
            'child_organizations': json.dumps(child_organizations),
            'organization':parent_organization,
            'username':parent_user_obj.username,
            'joined_date':parent_user_obj.date_joined.date,
            'organization_url': f"http://127.0.0.1:8000/suggestion/{parent_slug_name}/{parent_organization.id}/",
            'parent_name':parent_name   
            
        }
        return render(request, 'organization/organization_detail.html', context)


    else:
        #Code for the child organization
        organization=Organization.objects.filter(user=request.user).first()
        name=organization.name
        slug_name=slugify(name)
        user_obj=User.objects.get(id=organization.user.id)
        context = {
            'organization': organization,
            'username':user_obj.username,
            'joined_date':user_obj.date_joined.date,
            'organization_url': f"http://127.0.0.1:8000/suggestion/{slug_name}/{organization.id}/",
            'name':name
        }
        return render(request, 'organization/organization_detail.html', context)





# Code for displaying the initial page 
def home (request):
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
                messages.success(request,"Logged in successfully.")
                return HttpResponseRedirect("/")
             
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
            return redirect(reversed('login'))
        else:
            messages.error(request,"Invalid data, Please try again")
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
        parent_organization_obj=Organization.objects.filter(user=user,parent_id=None)
        if parent_organization_obj.exists():
            #code for the parent organization
            feedback_context={}
            parent_organization=parent_organization_obj.first()
            child_organization_id=Organization.objects.filter(parent_id=parent_organization.id).values_list('id', flat=True)
        
            forward_feedback_id=Forward.objects.filter(organization_id__in=child_organization_id).values_list('feedback_id', flat=True)

            similar_id=Similarity.objects.filter().values_list('similar_feedback_id',flat=True)
            
            feedback_objs=Feedback.objects.filter(id__in=forward_feedback_id,status=None)
            if feedback_objs.exists():
                for organization_id in child_organization_id:
                    feedback_by_organization=feedback_objs.filter(organization_id=organization_id)
                    feedback_list=[]
                    if feedback_by_organization.exists():
                        organization_name=Organization.objects.get(id=organization_id).name
                        for feedback in feedback_by_organization:
                                similarity_count=Similarity.objects.filter(feedback_id=feedback.id).count()
                                feedback_list.append({
                                'id':feedback.id,        
                                'feedback': feedback.feedback,
                                'date': feedback.date,
                                'sender': feedback.sender_id.name,
                                'status': feedback.status,
                                'similarity_count':similarity_count
                                })
                        feedback_context[organization_name] = feedback_list

            #Code for the suggestion send by the parent organization qr
            similar_id=Similarity.objects.filter().values_list('similar_feedback_id',flat=True).exclude(similar_feedback_id__isnull=True)
            feedbacks_by_topic = Feedback.objects.filter(organization_id=organization) \
                                                .values('topic_id') \
                                                .annotate(feedback_count=Count('id')) \
                                                .order_by('-feedback_count') \
                                                .exclude(id__in=similar_id)
            if feedbacks_by_topic.exists():
                   
                    for topic_feedback in feedbacks_by_topic:
                        topic_id = topic_feedback['topic_id']
                        topic_name = Topic.objects.get(id=topic_id).topic
                        feedbacks = Feedback.objects.filter(organization_id=organization, topic_id=topic_id,status=None).exclude(id__in=similar_id)
                        feedback_list = []
                        forward_feedback_list=[]
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
            
            
        else:
            #Code for the child organization
            if (organization):

                similar_id=Similarity.objects.filter().values_list('similar_feedback_id',flat=True).exclude(similar_feedback_id__isnull=True)
                feedbacks_by_topic = Feedback.objects.filter(organization_id=organization) \
                                                .values('topic_id') \
                                                .annotate(feedback_count=Count('id')) \
                                                .order_by('-feedback_count')\
                                                .exclude(id__in=similar_id)
                if feedbacks_by_topic.exists():
                    feedback_context={}
                    for topic_feedback in feedbacks_by_topic:
                        topic_id = topic_feedback['topic_id']
                        topic_name = Topic.objects.get(id=topic_id).topic
                        feedbacks = Feedback.objects.filter(organization_id=organization, topic_id=topic_id,status=None).exclude(id__in=similar_id)
                        feedback_list = []
                        forward_feedback_list=[]
                        for feedback in feedbacks:
                            similarity_count=Similarity.objects.filter(feedback_id=feedback.id).count()
                            forward_feedback_objs=Forward.objects.filter(feedback_id=feedback.id)
                            if forward_feedback_objs:
                                forward_feedback_list.append({
                                    'id':feedback.id,        
                                    'feedback': feedback.feedback,
                                    'date': feedback.date,
                                    'sender': feedback.sender_id,
                                    'status': feedback.status,
                                    'similarity_count':similarity_count
                                    })
                            else:     
                                feedback_list.append({
                                    'id':feedback.id,        
                                    'feedback': feedback.feedback,
                                    'date': feedback.date,
                                    'sender': feedback.sender_id,
                                    'status': feedback.status,
                                    'similarity_count':similarity_count
                                    })
                                feedback_context[topic_name] = feedback_list     
                    return render(request,'organization/feedback.html',{"feedback_context":feedback_context,'forward_feedback_list':forward_feedback_list})
                return render(request,'organization/feedback.html',{"feedback_context":{}})         
                    # Retrieve the feedbacks for this specific topic
    except organization.DoesNotExist:
        organization=None  





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
                sender_id_list=[]
                feedback_obj=Feedback.objects.get(id=feedback_id)
                print("done")
                feedback_obj.status=True
                feedback_obj.save()
                #Code to send the email
                sender_id_list.append(feedback_obj.sender_id)
                similar_senders = Similarity.objects.filter(feedback_id=feedback_id)
                for similar_sender_obj in similar_senders:
                    sender_obj=Sender.objects.get(id=similar_sender_obj.sender_id.id)
                    sender_id_list.append(sender_obj)
                for sender in sender_id_list:
                    recipient_list=[]
                    sender_obj=Sender.objects.get(id=sender.id)
                    sender_email=sender_obj.email
                    recipient_list.append(sender_email)
                    sender_name=sender_obj.name
                    context={
                          'name':sender_name,
                          'feedback':feedback_obj.feedback,
                          'response_message':response_message
                         
                    }
                    html_content = render_to_string('organization/feedback_solved_mail.html', context)
                    subject = "Suggestion" 
                #send_email_to_client function is in the utils.py file
                    email_thread = EmailThread(subject, html_content, recipient_list)
                    email_thread.start()
                return JsonResponse({'status': 'success', 'message': 'Response send successfully'})

            #Code to handle the unable to solve 
            elif dropdown_clicked_id == 1:
                sender_id_list=[]
                feedback_obj=Feedback.objects.get(id=feedback_id)
                feedback_obj.status=False
                feedback_obj.save()

                sender_id_list.append(feedback_obj.sender_id)
                similar_senders = Similarity.objects.filter(feedback_id=feedback_id)
                for similar_sender_obj in similar_senders:
                    sender_obj=Sender.objects.get(id=similar_sender_obj.sender_id.id)
                    sender_id_list.append(sender_obj)
                for sender in sender_id_list:
                    recipient_list=[]
                    sender_obj=Sender.objects.get(id=sender.id)
                    sender_email=sender_obj.email
                    recipient_list.append(sender_email)
                    sender_name=sender_obj.name
                    context={
                          'name':sender_name,
                          'feedback':feedback_obj.feedback,
                          'response_message':response_message    
                    }
                    html_content = render_to_string('organization/feedback_unsolved_mail.html', context)
                    subject = "Suggestion" 
                #send_email_to_client function is in the utils.py file
                    email_thread = EmailThread(subject, html_content, recipient_list)
                    email_thread.start()
                return JsonResponse({'status': 'success', 'message': 'Response send successfully'})
            

            #Cod to handle the forward the feedback to the parent
            elif dropdown_clicked_id == 2:
              
                sender_id_list=[]
                forward=Forward()
                feedback_obj=Feedback.objects.get(id=feedback_id)
                forward.feedback_id=feedback_obj
                forward.organization_id=Organization.objects.get(user=request.user)
                forward.save()

                sender_id_list.append(feedback_obj.sender_id)
                similar_senders = Similarity.objects.filter(feedback_id=feedback_id)
                for similar_sender_obj in similar_senders:
                    sender_obj=Sender.objects.get(id=similar_sender_obj.sender_id.id)
                    sender_id_list.append(sender_obj)
                for sender in sender_id_list:
                    recipient_list=[]
                    sender_obj=Sender.objects.get(id=sender.id)
                    sender_email=sender_obj.email
                    recipient_list.append(sender_email)
                    sender_name=sender_obj.name
                    parent_id=Organization.objects.get(user=request.user).parent_id
                    parent_obj=Organization.objects.get(id=parent_id)
                    
                    context={
                          'name':sender_name,
                          'feedback':feedback_obj.feedback,
                          'response_message':response_message,
                          'parent_name':parent_obj.name  
                    }
                    html_content = render_to_string('organization/feedback_forward_mail.html', context)
                    subject = "Suggestion" 
                #send_email_to_client function is in the utils.py file
                    email_thread = EmailThread(subject, html_content, recipient_list)
                    email_thread.start()
                return JsonResponse({'status': 'success', 'message': 'Suggestion forwarded successfully'})
                
           
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
 
@login_required
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
@login_required
@csrf_exempt 
def multi_department(request):
    if request.method == 'POST':
        department_data = []
        existing_users = []

        # Collecting data from the POST request
        for key in request.POST:
            if key.startswith('name_'):
                index = key.split('_')[1]
                authenticated_sender = request.POST.get(f'authenticated_sender_{index}') == '1'  # Convert to boolean
                department = {
                    'index': index,
                    'name': request.POST[f'name_{index}'],
                    'email': request.POST[f'email_{index}'],
                    'authenticated_sender': authenticated_sender
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

                # Code for sending the email to each department with their login credentials
                recipient_list = [username]
                parent_name = parent_organization.name
                context = {
                    'username': username,
                    'password': password,
                    'name': name,
                    'parent_name': parent_name
                }
                html_content = render_to_string('organization/user_create_mail.html', context)
                subject = "Account Created Successfully"
                # send_email_to_client function is in utils.py file
                email_thread = EmailThread(subject, html_content, recipient_list)
                email_thread.start()
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
    try:
        user_obj=request.user
        organization_obj=Organization.objects.get(user=user_obj)
        
    except organization_obj.DoesNotExist:
        messages.info(request,"Please register your Organization.")
        return HttpResponseRedirect("organization_register")

#Code for the parent organization
    organization_child_obj=Organization.objects.filter(parent_id=organization_obj.id)
    if organization_child_obj.exists():
        child_ids = organization_child_obj.values_list('id', flat=True)
        child_feedback_objs = Feedback.objects.filter(
    Q(organization_id__in=child_ids) | Q(organization_id=organization_obj)
)
        total_count=0
        solved_count=0
        latest_suggestion_list=[]
        frequent_suggestions=[]
        statistics=[]
        feedback_obj=Feedback.objects.filter(organization_id=organization_obj)
        for feedback in child_feedback_objs:
            forward_obj=Forward.objects.filter(feedback_id=feedback)
            if forward_obj.exists():
                total_count+=1
                if feedback.status:
                    solved_count+=1
        for feedback in feedback_obj:
            total_count+=1
            if feedback.status:
                solved_count+=1
        latest_feedback_obj=child_feedback_objs.order_by("-date")
        ordered_feedback_obj=feedback_obj.order_by("-date")
        latest_suggestion_list=[]
        for latest_feedback in latest_feedback_obj:
            forward_obj=Forward.objects.filter(feedback_id=latest_feedback)
            if forward_obj.exists():
                if   latest_feedback.status is None and len(latest_suggestion_list)<=3:
                    sender=latest_feedback.sender_id
                    suggestion={
                        "user":sender.name,
                        "time":latest_feedback.date,
                        "feedback":latest_feedback.feedback,
                        "forward_from":latest_feedback.organization_id.name,
                        "id":latest_feedback.id
                    }
                    latest_suggestion_list.append(suggestion)
        for latest_feedback in ordered_feedback_obj:
            if   latest_feedback.status is None and len(latest_suggestion_list)<=3:
                sender=latest_feedback.sender_id
                suggestion={
                        "user":sender.name,
                        "time":latest_feedback.date,
                        "feedback":latest_feedback.feedback,
                        "id":latest_feedback.id
                    }
                latest_suggestion_list.append(suggestion)
        #Code for the frequent suggestion            

        feedbacks_by_topic = feedback_obj \
                                             .values('topic_id') \
                                             .annotate(feedback_count=Count('id')) \
                                             .order_by('-feedback_count')[:3]    
        for feedback in feedbacks_by_topic:
            topic_obj=Topic.objects.get(id=feedback['topic_id'])
            topic=topic_obj.topic
            feedback_obj=Feedback.objects.filter(topic_id=topic_obj,status=None,organization_id=organization_obj)
            feedback_count_by_topic=feedback_obj.count()
            latest_time_obj=feedback_obj.order_by("-date").first()
            if latest_time_obj:
                suggestion={
                    'topic':topic,
                    "count":feedback_count_by_topic,
                    "latest_time":latest_time_obj.date
                }
                frequent_suggestions.append(suggestion)  
            today = timezone.now()
        start_of_week = today - timedelta(days=today.weekday())
        
        weeks = [start_of_week - timedelta(weeks=i) for i in range(4)]
        week_labels = [f"Week {i+1}" for i in range(4)]
        feedback_obj=Feedback.objects.filter(organization_id=organization_obj)
        week_counts = [
            feedback_obj.filter(date__gte=weeks[i], date__lt=weeks[i] + timedelta(weeks=1)).count()
            for i in range(4)
        ]
        
        statistics = {
            'labels': week_labels,
            'values': week_counts,
        }                     
        context = {
              # Update with the actual path or URL to the logo image
            'problems_count': total_count,
            'solved_count': solved_count,
            'latest_suggestion':latest_suggestion_list,
            'frequent_suggestions': frequent_suggestions,
            'statistics': statistics,
            'parent':True
        }
        return render(request, 'organization/dashboard.html', context)                
        
    else:
        #code for the child organization
        latest_suggestion_list=[]
        frequent_suggestions=[]
        feedback_obj=Feedback.objects.filter(organization_id=organization_obj)
        problem_count=feedback_obj.count
        solved_count=feedback_obj.filter(status=True).count()
        forward_feedback_ids=Forward.objects.filter(organization_id=organization_obj).values_list('feedback_id', flat=True)
        feedback_obj=feedback_obj.filter(status=None).exclude(id__in=forward_feedback_ids)
        latest_suggestion_obj=feedback_obj.order_by("-date")[:4]
        for latest_suggestion in latest_suggestion_obj:
            sender=latest_suggestion.sender_id
            suggestion={
                "user":sender.name,
                "time":latest_suggestion.date,
                "feedback":latest_suggestion.feedback,
                'id':latest_suggestion.id
            }
            latest_suggestion_list.append(suggestion)
        feedbacks_by_topic = feedback_obj \
                                             .values('topic_id') \
                                             .annotate(feedback_count=Count('id')) \
                                             .order_by('-feedback_count')[:3]    
        for feedback in feedbacks_by_topic:
            topic_obj=Topic.objects.get(id=feedback['topic_id'])
            topic=topic_obj.topic
            feedback_obj=Feedback.objects.filter(topic_id=topic_obj,status=None,organization_id=organization_obj)
            feedback_count_by_topic=feedback_obj.count()
            latest_time_obj=feedback_obj.order_by("-date").first()
            if latest_time_obj:
                suggestion={
                    'topic':topic,
                    "count":feedback_count_by_topic,
                    "latest_time":latest_time_obj.date
                }
                frequent_suggestions.append(suggestion)
                
        today = timezone.now()
        start_of_week = today - timedelta(days=today.weekday())
        
        weeks = [start_of_week - timedelta(weeks=i) for i in range(4)]
        week_labels = [f"Week {i+1}" for i in range(4)]
        feedback_obj=Feedback.objects.filter(organization_id=organization_obj)
        week_counts = [
        feedback_obj.filter(date__gte=weeks[i], date__lt=weeks[i] + timedelta(days=7)).count()
        for i in range(4)
]
        
        statistics = {
            'labels': week_labels,
            'values': week_counts,
        }  
        
        context = {
           # Update with the actual path or URL to the logo image
            'problems_count': problem_count,
            'solved_count': solved_count,
            'latest_suggestion':latest_suggestion_list,
            'frequent_suggestions': frequent_suggestions,
            'statistics': statistics
        }
        return render(request, 'organization/dashboard.html', context)


#Code for the Insights
@login_required
def insights(request):
    user_obj=request.user
    organization_obj=Organization.objects.get(user=user_obj)
    organization_child_obj=Organization.objects.filter(parent_id=organization_obj.id)
    if organization_child_obj.exists():
        labels=[]
        total_feedback=[]
        solved_feedback=[]
        departments=[]
        for department in organization_child_obj:
            feedback_obj=Feedback.objects.filter(organization_id=department)
            total_feedback_count=feedback_obj.count()
            solved_feedback_count=feedback_obj.filter(status=True).count()
            department_name=department.name
            labels.append(department_name)
            total_feedback.append(total_feedback_count)
            solved_feedback.append(solved_feedback_count)
            department={
            "id":department.id,
            "name":department.name
        }
            departments.append(department)
          
        department_double_statistics={
            "labels":labels,
            "value_a":total_feedback,
            "value_b":solved_feedback
        }

        # Code for sending the department performance for the initial render of the parent_insights.html
        feedback_obj=Feedback.objects.filter(organization_id=organization_child_obj.first().id)
        feedbacks_by_topic = feedback_obj \
                                             .values('topic_id') \
                                             .annotate(feedback_count=Count('id')) \
                                             .order_by('-feedback_count')[:3]
        labels=[]
        total_feedback=[]
        solved_feedback=[]
        for feedback in feedbacks_by_topic:
            topic_id=feedback['topic_id']
            topic_name=Topic.objects.get(id=topic_id).topic
            total_feedback_count=feedback['feedback_count']
            solved_feedback_count=feedback_obj.filter(topic_id=topic_id,status=True).count()
            labels.append(topic_name)
            total_feedback.append(total_feedback_count)
            solved_feedback.append(solved_feedback_count)
        statistics={
              "labels":labels,
              "values":total_feedback
        }

        double_statistics={
            "labels":labels,
            "value_a":total_feedback,
            "value_b":solved_feedback
        }
        
        
        context = {
        'department_double_statistics':json.dumps(department_double_statistics),
        'statistics':json.dumps(statistics),
        'double_statistics':json.dumps(double_statistics),
        'departments':departments,
        'department_name':organization_child_obj.first().name

        }
        
        #code for the parent organization
        return render(request, 'organization/parent_insights.html', context)
       
    else:
        #Code for the child organization
        feedback_obj=Feedback.objects.filter(organization_id=organization_obj)
        feedbacks_by_topic = feedback_obj \
                                             .values('topic_id') \
                                             .annotate(feedback_count=Count('id')) \
                                             .order_by('-feedback_count')[:3]
        labels=[]
        total_feedback=[]
        solved_feedback=[]
        for feedback in feedbacks_by_topic:
            topic_id=feedback['topic_id']
            topic_name=Topic.objects.get(id=topic_id).topic
            total_feedback_count=feedback['feedback_count']
            solved_feedback_count=feedback_obj.filter(topic_id=topic_id,status=True).count()
            labels.append(topic_name)
            total_feedback.append(total_feedback_count)
            solved_feedback.append(solved_feedback_count)
        statistics={
              "labels":labels,
              "values":total_feedback
        }

        double_statistics={
            "labels":labels,
            "value_a":total_feedback,
            "value_b":solved_feedback
        }
        
        context = {
            'statistics': json.dumps(statistics),
            'double_statistics': json.dumps(double_statistics)
        }
        

        return render(request, 'organization/insights.html', context)

#Code to handle the department clicked in the parent_insights        
@csrf_exempt          
def handle_department_action(request):
        data = json.loads(request.body)
        department_id=data.get("department_id")
        organization_obj=Organization.objects.get(id=department_id)
        feedback_obj=Feedback.objects.filter(organization_id=organization_obj)
        feedbacks_by_topic = feedback_obj \
                                             .values('topic_id') \
                                             .annotate(feedback_count=Count('id')) \
                                             .order_by('-feedback_count')[:3]
        labels=[]
        total_feedback=[]
        solved_feedback=[]
        for feedback in feedbacks_by_topic:
            topic_id=feedback['topic_id']
            topic_name=Topic.objects.get(id=topic_id).topic
            total_feedback_count=feedback['feedback_count']
            solved_feedback_count=feedback_obj.filter(topic_id=topic_id,status=True).count()
            labels.append(topic_name)
            total_feedback.append(total_feedback_count)
            solved_feedback.append(solved_feedback_count)
        statistics={
              "labels":labels,
              "values":total_feedback
        }

        double_statistics={
            "labels":labels,
            "value_a":total_feedback,
            "value_b":solved_feedback
        }
        


        context = {
            'statistics': statistics,
            'double_statistics': double_statistics,
            'department_name':organization_obj.name
        }
       
        return JsonResponse({"context":context})


#Function for the settings 
@login_required
def account_settings(request):
    try:
        suggestion_box_status = get_suggestion_box_status(request)
        if suggestion_box_status is None:
            messages.info(request, "Please register the organization first.")
            return redirect(reverse('organization_register'))
        else:
            form = MyPasswordChangeForm(user=request.user)
            logo_form=OrganizationLogoForm
            return render(request, 'organization/settings.html',{'form':form,'logo_form':logo_form})
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return render(request, 'organization/settings.html')



@login_required
def edit_account(request):
    try:
        suggestion_box_status = get_suggestion_box_status(request)
        if suggestion_box_status is None:
            return JsonResponse({'error': 'Please register the organization first.'}, status=400)

        if request.method == "GET" :
            organization_obj = Organization.objects.filter(user=request.user).first()
            if organization_obj:
                
                data = {
                    'name': organization_obj.name,
                    'authenticated_sender': organization_obj.authenticated_sender,
                    'email':request.user.username
                }
                
                return JsonResponse(data)
            else:
                return JsonResponse({'error': 'Organization not found.'}, status=404)
        elif request.method == "POST":
            print("post_clicked_form_edit_photo")
            delete_account=request.POST.get('_method')
            if delete_account:
                organization_obj = Organization.objects.filter(user=request.user).first()
                # organization_obj.delete()
                messages.success(request, "Account deleted successfully.")
                return redirect(reverse('home'))
            
            elif 'logo' in request.FILES:
                organization = Organization.objects.filter(user=request.user).first()
                logo_form = OrganizationLogoForm(request.POST, request.FILES, instance=organization)
                if logo_form.is_valid():
                    # Delete the old logo file
                    old_logo_path = organization.logo.path
                    if os.path.isfile(old_logo_path):
                        os.remove(old_logo_path)

                    logo_form.save()
                    messages.success(request, 'Your logo was successfully updated!')
                    return redirect('account_settings')
                else:
                    messages.error(request, 'Please correct the error below.')
            else:
                organization_obj = Organization.objects.filter(user=request.user).first()
                name = request.POST.get('name')
                authenticated_sender = request.POST.get('authenticated_sender')
                email=request.POST.get('email')
                organization_obj.name = name
                organization_obj.authenticated_sender = authenticated_sender
                request.user.username=email
                request.user.save()
                organization_obj.save()
                messages.success(request, "Account information updated successfully.")
                return redirect('account_settings')
        

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




#Function for password change done

def password_change_done(request):
    messages.success(request,"Password changed successfully. Please use new password to login.")
    return redirect(reverse('login'))


#Function for the qr_code rendering 
def get_organization_qr_templates(request):
    return render(request,'organization/organization_qr.html')



#Function for the similarity feedback rendering
@csrf_exempt
def get_similar_feedback(request):
    if request.method=="POST":
        data = json.loads(request.body)
        feedback_id = data.get('feedback_id')
        similar_feedback_ids=Similarity.objects.filter(feedback_id=feedback_id).values_list("similar_feedback_id",flat=True)
        similar_feedback_objs=Feedback.objects.filter(id__in=similar_feedback_ids)
        similar_feedbacks=[]
        for similar_feedbck_obj in similar_feedback_objs:
            sender_obj=Sender.objects.filter(id=similar_feedbck_obj.sender_id.id).first()
            feedback={
                "feedback":similar_feedbck_obj.feedback,
                "date":similar_feedbck_obj.date,
                "sender":sender_obj.name
            }
            similar_feedbacks.append(feedback)
        return JsonResponse({"similar_feedbacks":similar_feedbacks})   
        
        

    
