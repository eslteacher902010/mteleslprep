from django.urls import path
from . import views

urlpatterns = [
    # Home / static pages
    path('', views.home, name='home'),
    path('practice/', views.practice, name='practice'),
    path('about/', views.about, name='about'),
    path('addq/', views.add_question, name='add-question'),
    # path('login/', views.CustomLoginView.as_view(), name='login'),
    

    # All questions 
    path('questions/', views.question_index, name='question-index'),

    # Short answer list 
    path('questions/short/', views.ShortQuestionList.as_view(), name='short-index'),
    path('questions/short/<int:pk>/', views.ShortQuestionDetail.as_view(), name='short-detail'),
    path('questions/short/create/', views.ShortAnswerQuestionCreate.as_view(), name='short-create'),
    path('questions/short/<int:pk>/update/', views.ShortAnswerQuestionUpdate.as_view(), name='short-update'),
    path('questions/short/<int:pk>/delete/', views.ShortAnswerQuestionDelete.as_view(), name='short-delete'),

 

    # Long answer 
    path('questions/long/', views.LongQuestionList.as_view(), name='long-index'),
    path('questions/long/<int:pk>/', views.LongQuestionDetail.as_view(), name='long-detail'),
    path('questions/long/create/', views.LongAnswerQuestionCreate.as_view(), name='long-create'),
    path('questions/long/<int:pk>/update/', views.LongAnswerQuestionUpdate.as_view(), name='long-update'),
    path('questions/long/<int:pk>/delete/', views.LongAnswerQuestionDelete.as_view(), name='long-delete'),


    # Multiple choice  
    path('questions/mcq/', views.MCQList.as_view(), name='mcq-index'),
    path('questions/mcq/<int:pk>/', views.MCQDetail.as_view(), name='mcq-detail'),
    path('questions/mcq/create/', views.MultipleChoiceQuestionCreate.as_view(), name='mcq-create'),
    path('questions/mcq/<int:pk>/update/', views.MultipleChoiceQuestionUpdate.as_view(), name='mcq-update'),
    path('questions/mcq/<int:pk>/delete/', views.MultipleChoiceQuestionDelete.as_view(), name='mcq-delete'),


    path('accounts/signup/', views.signup, name='signup'),

    # # Create / update / delete 
    # path('questions/create/', views.QuestionCreate.as_view(), name='question-create'),
    # path('questions/<int:pk>/update/', views.QuestionUpdate.as_view(), name='question-update'),
    # path('questions/<int:pk>/delete/', views.QuestionDelete.as_view(), name='question-delete'),
]
