from datetime import datetime, date, time
from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def activity_time(value):

    if not value:
        return ""

    # Convert DateField to DateTime
    if isinstance(value, date) and not isinstance(value, datetime):
        value = datetime.combine(value, time.min)
        value = timezone.make_aware(value)

    now = timezone.now()

    diff = now - value

    seconds = diff.total_seconds()

    if seconds < 60:
        return "Just now"

    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} min ago"

    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} hr ago"

    elif seconds < 172800:
        return "Yesterday"

    elif seconds < 604800:
        return f"{diff.days} days ago"

    else:
        return value.strftime("%d %b %Y")