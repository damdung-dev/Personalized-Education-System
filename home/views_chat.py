# views_chat.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# import model trả lời chat


def chat_page(request):
    """
    Trang hiển thị giao diện chat (GET)
    """
    return render(request, "home/chat.html", {})


@csrf_exempt
def chat_api(request):
    """
    API nhận message từ frontend và trả response từ AI model
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            user_message = data.get("message", "")
            
            if not user_message.strip():
                return JsonResponse({"error": "Empty message"}, status=400)
            
            # gọi model
            bot_reply = generate_response(user_message)

            return JsonResponse({
                "message": user_message,
                "reply": bot_reply
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)
