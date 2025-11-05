from django.urls import path
from . import views

urlpatterns = [
    # Home / static pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('addq/', views.add_question, name='add-question'),
    path('accounts/signup/', views.signup, name='signup'),
    # path('login/', views.CustomLoginView.as_view(), name='login'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    

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




    #associations 
    path('practice/<int:practice_id>/associate-question/<int:question_id>/question_type/<str:question_type>/', views.associate_question, name='associate-question'),

    # Practice tests
    path('practice-tests/', views.PracticeTestList.as_view(), name='practice-test-index'),
    path('practice-tests/<int:practice_id>/', views.practice_test_detail, name='practice-detail'),
    path('practice-tests/create/', views.CreatePracticeTest.as_view(), name='practice-test-create'),
    path('practice-tests/<int:pk>/update/', views.UpdatePracticeTest.as_view(), name='practice-test-update'),
    path('practice-tests/<int:pk>/delete/', views.DeletePracticeTest.as_view(), name='practice-test-delete'),
    path('practice-tests/<int:practice_test_id>/take/', views.take_practice_test, name='practice-take'),
    path('practice-tests/<int:practice_test_id>/results/', views.practice_results, name='practice-results'),
    path('practice/<int:test_id>/next/<int:q_num>/', views.next_question, name='next_question'),
    path('practice/check_answer/<int:question_id>/', views.check_answer, name='check-answer')






    # # Create / update / delete 
    # path('questions/create/', views.QuestionCreate.as_view(), name='question-create'),
    # path('questions/<int:pk>/update/', views.QuestionUpdate.as_view(), name='question-update'),
    # path('questions/<int:pk>/delete/', views.QuestionDelete.as_view(), name='question-delete'),
]
