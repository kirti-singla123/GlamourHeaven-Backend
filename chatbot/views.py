from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from groq import Groq

from .knowledge_base import SYSTEM_PROMPT

GROQ_MODEL = "llama-3.1-8b-instant"
MAX_HISTORY_MESSAGES = 10

_client = None


def get_groq_client():
    global _client
    if _client is None:
        if not settings.GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY is not configured.")
        _client = Groq(api_key=settings.GROQ_API_KEY)
    return _client


@api_view(['POST'])
@permission_classes([AllowAny])
def chat(request):
    user_message = (request.data.get('message') or '').strip()
    if not user_message:
        return Response({'error': 'message is required'}, status=status.HTTP_400_BAD_REQUEST)

    history = request.data.get('history') or []
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if isinstance(history, list):
        for entry in history[-MAX_HISTORY_MESSAGES:]:
            role = entry.get('role') if isinstance(entry, dict) else None
            content = entry.get('content') if isinstance(entry, dict) else None
            if role in ('user', 'assistant') and content:
                messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_message})

    try:
        client = get_groq_client()
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=512,
        )
        reply = completion.choices[0].message.content
    except Exception as e:
        print("Groq chatbot error:", e)
        return Response(
            {'error': 'Failed to get a response from the chatbot. Please try again later.'},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    return Response({'reply': reply}, status=status.HTTP_200_OK)
