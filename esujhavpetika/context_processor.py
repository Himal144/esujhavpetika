from organization.models import Organization,Feedback,Forward
from django.contrib.auth.models import User
from django.utils.text import slugify


def get_suggestion_box_status(request):
    if request.user.is_authenticated:
        organization_obj=Organization.objects.filter(user=request.user)
        status=None
        if organization_obj.exists():
            parent_organization_obj=organization_obj.filter(parent_id=None)
            if parent_organization_obj.exists():
                status=True
            else:
                status=False    
        return status
       
def get_organization_logo_url(request):
    if request.user.is_authenticated:
        user_obj=User.objects.get(id=request.user.id)
        organization_obj=Organization.objects.filter(user=user_obj).first()
        if organization_obj:
           logo_url=organization_obj.logo
           return logo_url   
       
def get_suggestion_box_count(request):
    if request.user.is_authenticated:
        suggestion_count=0
        user_obj=User.objects.get(id=request.user.id)
        organization_obj=Organization.objects.filter(user=user_obj).first()
        if organization_obj:
            suggestion_count=Feedback.objects.filter(organization_id=organization_obj,status=None).count()
            child_organization_objs=Organization.objects.filter(parent_id=request.user.id)
            for child_organization_obj in child_organization_objs:
                forward_objs=Forward.objects.filter(organization_id=child_organization_obj)
                for forward_obj in forward_objs:
                    feedback_obj=Feedback.objects.filter(id=forward_obj.feedback_id.id,status=None)
                    if feedback_obj is not None:
                        suggestion_count+=1
            return suggestion_count
   
def global_context(request):
    suggestion_box_status=get_suggestion_box_status(request)
    logo_url=get_organization_logo_url(request)
    if request.user.is_authenticated:
        suggestion_box_count=get_suggestion_box_count(request)
        organization_obj=Organization.objects.filter(user=request.user).first()
        slug_name=''
        id=None
        if organization_obj:
            slug_name=slugify(organization_obj.name)
            id=organization_obj.id 
        context={
                'suggestion_box_status':suggestion_box_status,
                'logo_url':logo_url,
                'slug_name':slug_name,
                'id':id 
            } 
    else:
        context={
                'suggestion_box_status':suggestion_box_status,
                'logo_url':logo_url,
            }      
    return context