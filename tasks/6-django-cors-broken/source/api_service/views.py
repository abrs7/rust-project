from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def status_view(request):
    """Simple status endpoint"""
    return JsonResponse({"status": "ok"})

@csrf_exempt
def data_view(request):
    """Data endpoint that should support CORS"""
    return JsonResponse({"message": "Hello from API"})