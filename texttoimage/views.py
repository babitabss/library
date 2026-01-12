from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import requests 
import json
from django.views.decorators.csrf import csrf_exempt

def image_page(request):
    return render(request, "form.html")

@csrf_exempt
def generate_image(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        body = json.loads(request.body.decode("utf-8"))
        prompt = body.get("prompt", "").strip()

        if not prompt:
            return JsonResponse({"error": "Prompt cannot be empty"}, status=400)

        # 🔹 Use real API here
        response = requests.post(
            url='https://taiapi.aiphotocraft.com/api/texttoimg',  # ✅ Fix URL (remove double https)
            headers={
                "Content-Type": "application/json",
                "x-api-key": settings.TEXT_TO_IMAGE_API_KEY,  # Make sure you added it in settings.py
                "x-source": "web"
            },
            json={"prompt": prompt},
            timeout=30
        )

        if response.status_code != 200:
            return JsonResponse({
                "error": f"API returned status {response.status_code}",
                "details": response.text
            }, status=response.status_code)

        data = response.json()
        return JsonResponse(data)

    except Exception as e:
        # 🔹 Show exact error for debugging
        return JsonResponse({"error": f"Internal Server Error: {str(e)}"}, status=500)