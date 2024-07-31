# organization/templatetags/custom_filters.py
from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.filter
def custom_timesince(value):
    if not value:
        return ""

    now = timezone.now()
    diff = now - value

    if diff < timedelta(days=1):
        hours = diff.seconds // 3600
        minutes=diff.seconds // 60
        if minutes < 60:
            return f"{minutes} minutes ago"
        else:
            if hours == 1:
                return "1 hour ago"
            return f"{hours} hours ago"
    else:
        days = diff.days
        if days == 1:
            return "1 day ago"
        return f"{days} days ago"
