"""
URL configuration for advanced_project_lab project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from chatgpt import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ask/', views.AskQuestionView.as_view(), name='ask-question'),
    path('response/<int:pk>/', views.GetResponseView.as_view(), name='get-response'),
    path('summary/', views.SummaryView.as_view(), name='summary'),  # 새로 추가된 URL
    path('reset/', views.ResetConversationView.as_view(), name='reset-conversation'),
]
