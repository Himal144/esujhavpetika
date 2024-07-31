from django.urls import path
from . import views 

urlpatterns = [
    path('<slug:name>/<int:id>/',views.send_suggestion,name="send_suggestion"),
    path('check-profane/',views.check_profane,name="check_profane")
]
