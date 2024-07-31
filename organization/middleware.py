from django.shortcuts import redirect
from django.urls import reverse
from esujhavpetika.context_processor import get_suggestion_box_status
from django.contrib import messages

class CustomRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
       
        if  self.check_suggestion_box_status(request):
            messages.info(request,"Please register your organization first.")
            return redirect(reverse('organization_register'))

        response = self.get_response(request)
        return response

    def check_suggestion_box_status(self, request):
       
        excluded_urls = [
            '/organization/account/register', 
        ]

        if request.path.startswith('/organization') and request.user.is_authenticated :
                if not any(request.path.startswith(url) for url in excluded_urls) and not request.path.startswith('/organization/account') :
                    status=get_suggestion_box_status(request)
                    if status is None:
                        return True
                    else:
                        return False
                elif(request.path.startswith('/organization/account')):
                    return False

        else:
            return False
                      
                
        