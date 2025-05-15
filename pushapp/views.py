from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from webpush import send_user_notification
from .models import PushSubscription
import json

@csrf_exempt
def save_info_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        endpoint = data.get("endpoint")
        keys = data.get("keys", {})
        p256dh = keys.get("p256dh")
        auth = keys.get("auth")

        if request.user.is_authenticated:
            PushSubscription.objects.update_or_create(
                user=request.user,
                endpoint=endpoint,
                defaults={"p256dh": p256dh, "auth": auth}
            )
            return JsonResponse({"status": "saved"})
        return JsonResponse({"status": "unauthenticated"}, status=403)
    return JsonResponse({"status": "bad request"}, status=400)

@login_required
def send_push(request):
    payload = {
        "head": "Новое видео!",
        "body": "Появился новый хайлайт на BESTMOMENTS.",
        "icon": "/static/img/logo.png",
        "url": "/"  # куда ведёт уведомление
    }
    try:
        send_user_notification(user=request.user, payload=payload, ttl=1000)
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "failed", "reason": str(e)})
        