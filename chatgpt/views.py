import openai
from rest_framework import generics, status
from rest_framework.response import Response
from .models import UserQuestion
from .serializers import UserQuestionSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

openai.api_key = ""


# views.py

history = []

class AskQuestionView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = UserQuestion.objects.all()
    serializer_class = UserQuestionSerializer

    def perform_create(self, serializer):
        user_question = serializer.save()

        try:
            # 챗봇 응답 처리
            # history = user_question.conversation_history
            history.append({"role": "user", "content": user_question.question})  # 사용자의 질문을 히스토리에 추가

            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=history  # 대화 히스토리를 messages로 전송
            )

            response = completion.choices[0].message.content

            # 챗봇의 응답을 히스토리에 추가
            history.append({"role": "assistant", "content": response})

            user_question.response = response
            user_question.conversation_history = history  # 대화 히스토리 업데이트
            user_question.save()

            print(history)

            return Response({"id": user_question.id,
    "question": user_question.question,
    "response": response,
    "conversation_history": user_question.conversation_history})

        except openai.error.RateLimitError:
            user_question.delete()
            return Response({"error": "API rate limit exceeded."}, status=status.HTTP_429_TOO_MANY_REQUESTS)


class GetResponseView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = UserQuestion.objects.all()
    serializer_class = UserQuestionSerializer

class SummaryView(APIView):
    permission_classes = [AllowAny]
    queryset = UserQuestion.objects.all()
    serializer_class = UserQuestionSerializer

    def post(self, request, *args, **kwargs):
        # 특정 질문 설정
        specific_question = "지금까지 우리가 한 대화내용을 세 줄로 요약해줘. 보고서의 결론 부분처럼 요약해줘"

        # 대화 이력 가져오기
        # 여기서는 예시로 빈 리스트를 사용하겠습니다. 실제 구현에서는 적절한 방법으로 대화 이력을 가져와야 합니다.

        try:
            history.append({"role": "user", "content": specific_question})

            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=history
            )

            response = completion.choices[0].message.content
            print(history)

            # 이 부분에서 대화 이력을 저장할 수 있습니다. 예를 들어, UserQuestion 모델을 사용하여 저장할 수 있습니다.

            return Response({
                "question": specific_question,
                "response": response,
                "conversation_history": history
            })
        except openai.error.RateLimitError:
            return Response({"error": "API rate limit exceeded."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

class ResetConversationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Resetting the conversation history
        global history
        role = f'You are a {request.data["role"]} counselor'

        history.append({'role': 'system', 'content': role})
        history.append({'role': 'user', 'content': '점심메뉴 뭐 먹을지 고민돼.'})

        return Response({"message": f"Conversation history has been {role}."})