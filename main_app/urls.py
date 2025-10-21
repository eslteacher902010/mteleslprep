from django.urls import path
from . import views

urlpatterns = [
    # Home / static pages
    path('', views.Home.as_view(), name='home'),
    path('practice/', views.practice, name='practice'),
    path('about/', views.about, name='about'),

    # All questions index
    path('questions/', views.question_index, name='question-index'),

    # Short answer list + detail
    path('questions/short/', views.ShortQuestionList.as_view(), name='short-index'),
    path('questions/short/<int:pk>/', views.ShortQuestionDetail.as_view(), name='short-detail'),

    # Long answer detail
    path('questions/long/', views.LongQuestionList.as_view(), name='long-index'),
    path('questions/long/<int:pk>/', views.LongQuestionDetail.as_view(), name='long-detail'),

    # Multiple choice detail
    path('questions/mcq/', views.MCQList.as_view(), name='mcq-index'),
    path('questions/mcq/<int:pk>/', views.MCQDetail.as_view(), name='mcq-detail'),

    # Create / update / delete (MCQs for now)
    path('questions/create/', views.QuestionCreate.as_view(), name='question-create'),
    path('questions/<int:pk>/update/', views.QuestionUpdate.as_view(), name='question-update'),
    path('questions/<int:pk>/delete/', views.QuestionDelete.as_view(), name='question-delete'),
]
