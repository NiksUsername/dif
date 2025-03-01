import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
import smtplib
from email.message import EmailMessage

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def analyse(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST requests are allowed.")

    try:
        data = json.loads(request.body)
        logs = data.get('logs')
        recipient_email = data.get('email')
        if not logs or not recipient_email:
            return HttpResponseBadRequest("Missing 'logs' or 'email' in the request.")
    except Exception:
        return HttpResponseBadRequest("Invalid JSON data.")

    prompt = f"Please analyze the following logs and provide insights:\n{logs}"

    try:
        response = client.chat.completions.create(model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an assistant analyzing logs."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150)
        gpt_response = response.choices[0].message.content.strip()
    except Exception as e:
        return JsonResponse({
            "error": "Error communicating with ChatGPT",
            "details": str(e)
        }, status=500)


    email_subject = "ChatGPT Analysis Response"
    email_body = (
        f"Dear User,\n\n"
        f"Here is the analysis of your logs:\n\n{gpt_response}\n\n"
        "Best regards,\nYour Django App"
    )

    msg = EmailMessage()
    msg.set_content(email_body)
    msg['Subject'] = email_subject
    msg['From'] = os.getenv('EMAIL_HOST_USER')
    msg['To'] = recipient_email

    try:
        email_port = int(os.getenv('EMAIL_PORT', 587))
        with smtplib.SMTP(os.getenv('EMAIL_HOST'), email_port) as server:
            server.starttls()
            server.login(os.getenv('EMAIL_HOST_USER'), os.getenv('EMAIL_HOST_PASSWORD'))
            server.send_message(msg)
    except Exception as e:
        return JsonResponse({
            "error": "Failed to send email",
            "details": str(e)
        }, status=500)

    return JsonResponse({
        "message": "Analysis completed and email sent successfully",
        "analysis": gpt_response
    })
