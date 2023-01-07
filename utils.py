from django.http import JsonResponse


def catch_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return JsonResponse({"error": f"{e.__class__.__name__} : {e}"}, status=400)

    return wrapper
