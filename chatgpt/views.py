import openai
from rest_framework import generics, status
from rest_framework.response import Response
from .models import UserQuestion
from .serializers import UserQuestionSerializer
from rest_framework.permissions import AllowAny
import environ, os

env = environ.Env()
environ.Env.read_env()
openai.api_key = env('OPEN_API_KEY')


class AskQuestionView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = UserQuestion.objects.all()
    serializer_class = UserQuestionSerializer

    def perform_create(self, serializer):
        # 사용자 질문 저장
        user_question = serializer.save()

        try:
            # 챗봇 응답 처리
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_question.question}
            ]

            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            response = completion.choices[0].message.content
            user_question.response = response
            user_question.save()

            return Response({"id": user_question.id, "response": response})

        except openai.error.RateLimitError:
            user_question.delete()  # 오류가 발생했으므로 질문을 삭제합니다.
            return Response({"error": "API rate limit exceeded."}, status=status.HTTP_429_TOO_MANY_REQUESTS)


class GetResponseView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = UserQuestion.objects.all()
    serializer_class = UserQuestionSerializer
