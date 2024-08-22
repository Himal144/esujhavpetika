from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .forms import SuggestionForm
from organization.models import Organization, Topic,Feedback
from .models import Sender
from organization.models import Similarity
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
# from .profanity_check import check_profanity
# from .semantic_similarity import check_semantic_similarity,store_vector_of_suggestion 

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def send_suggestion(request,name,id):
    try:
        organization_obj = get_object_or_404(Organization, id=id)
        slug_name=slugify(organization_obj.name)
        if name != slug_name :
            return render(request, '404.html', status=404)
        topic_list = Topic.objects.filter(organization_id=organization_obj.id)
        if request.method == 'POST':
            form = SuggestionForm(request.POST, authenticated_sender=organization_obj.authenticated_sender)
            if form.is_valid():
                topic_name = form.cleaned_data['topic']
                topic, created = Topic.objects.get_or_create(topic=topic_name, defaults={'organization_id': organization_obj})
                suggestion=form.cleaned_data['suggestion']
    #Sending the suggestion to check the semantic similarity
                # id=check_semantic_similarity(suggestion)
                name=form.cleaned_data['name']
                email=form.cleaned_data['email']
                feedback_obj=Feedback()
                if (name or email):
                    if not name:
                        name="Anonymous"
                    sender_obj=Sender.objects.create(name=name,email=email)
                else:
                    sender_obj=Sender.objects.create(name="Anonymous",email='')
              
                if(not id):
                    #Code if the suggestion is not similar with other suggestion
                    feedback_obj.sender_id=sender_obj
                    feedback_obj.feedback=suggestion
                    feedback_obj.date=timezone.now()
                    feedback_obj.organization_id=organization_obj
                    feedback_obj.topic_id=topic
                    feedback_obj.status=None
                    feedback_obj.save()
                    # store_vector_of_suggestion(feedback_obj.id,suggestion)
                    messages.success(request,"Suggestion send successfully.")
                    return JsonResponse({'success': True,})

                else:
                    #code for if the suggestion is similar  with other suggestion
                    similar_feedback_obj=Feedback.objects.filter(id=id).first()
                    feedback_obj.sender_id=sender_obj
                    feedback_obj.feedback=suggestion
                    feedback_obj.date=timezone.now()
                    feedback_obj.organization_id=organization_obj
                    feedback_obj.topic_id=topic
                    feedback_obj.status=None
                    feedback_obj.save() 
                    Similarity.objects.create(feedback_id=similar_feedback_obj,sender_id=sender_obj,similar_feedback_id=feedback_obj)
                    messages.success(request,"Suggestion send successfully.")
                    return JsonResponse({'success': True,})
                # Save the suggestion
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
        else:
            form = SuggestionForm(authenticated_sender=organization_obj.authenticated_sender)
            
            context = {
                "organization_name": organization_obj.name,
                "authenticated_sender": organization_obj.authenticated_sender,
                "logo": organization_obj.logo.url,  # Assuming you have a URL for the logo
                "form": form,
                "topics": list(topic_list.values('topic')),  # Sending the list of topics to the template
                "organization_id":organization_obj.id,
                "slug_name":slug_name,

            }
            return render(request, 'user/suggestion_form.html', context)
    except json.JSONDecodeError:
         return JsonResponse({'success': False, 'error': 'Failed to send suggestion.Please try again'}, status=400)



#Code for checking the profanity 
# from better_profanity import profanity
import json
@csrf_exempt
def check_profane(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            suggestion = data.get('suggestion', '')
            # profane_result= profanity.contains_profanity(suggestion)
            # return JsonResponse({'success':profane_result})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)    
    


