from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout 
<<<<<<< HEAD
from .forms import signupform
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import send_email_to_client
=======
from .forms import signupform , organization_register_form
 

from . models import Organization
>>>>>>> origin/master

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
<<<<<<< HEAD
                messages.success(request,"Logged in successfully")
                return HttpResponseRedirect("/feedback")
=======
                return HttpResponseRedirect("/organization/register")
>>>>>>> origin/master
             
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

def user_logout(request):
    logout(request)
    messages.warning(request,"Log out succefully")
    return HttpResponseRedirect('/')

<<<<<<< HEAD
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
                subject="Feedback response"
                message="Your feedback is solved "

                sender_id_list=Similarity.objects.filter(feedback_id=feedback_id).values('sender_id')
                recipient_list=[]
                for sender in sender_id_list:
                    sender_obj=Sender.objects.get(id=sender["sender_id"])
                    sender_email=sender_obj.email
                    recipient_list.append(sender_email)
                    
                #send_email_to_client function is in the utils.py file
                send_email_to_client(subject,message,recipient_list)
               


            #Code to handle the unable to solve 
            elif dropdown_clicked_id == 1:
                feedback_obj=Feedback.objects.get(id=feedback_id)
                feedback_obj.status=False
                feedback_obj.save()
                #code to send the email
            #Cod to handle the forward the feedback to the parent
            elif dropdown_clicked_id == 2:
                print("done")
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
=======
 

def organization_register(request):
    try:
        organization = Organization.objects.get(user=request.user)
        form = organization_register_form(request.POST, request.FILES, instance=organization)
    except Organization.DoesNotExist:
        form = organization_register_form(request.POST, request.FILES)
    
    if request.method == 'POST':
        if form.is_valid():
            organization = form.save(commit=False)
            organization.user = request.user
            organization.save()
            return HttpResponseRedirect('/')
    else:
          form = organization_register_form()    
    
    return render(request, 'organization/register.html', {'organization_register_form': form})

def multi_department(request):
    if request.method == 'POST':
        try:
            organization = Organization.objects.get(user=request.user)
            form = organization_register_form(request.POST, request.FILES, instance=organization)
        except Organization.DoesNotExist:
            form = organization_register_form(request.POST, request.FILES)
        
        if form.is_valid():
            organization = form.save(commit=False)
            organization.user = request.user
            organization.save()
            return JsonResponse({'success': True})  # Return success response for AJAX
            
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})  # Return errors for AJAX
    else:
        form = organization_register_form()   

    context = {
        'organization_register_form': form
    }
    
    return render(request, 'organization/multi_department.html', context)
>>>>>>> origin/master
