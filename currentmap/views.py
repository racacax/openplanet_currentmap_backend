from django.http import JsonResponse


def handler500(request, *args, **kwargs):
    return JsonResponse({"error": 500})