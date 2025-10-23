from urllib import request
from django.shortcuts import redirect, render, get_object_or_404


from django.views.generic.edit import CreateView

from django.views.generic import ListView, DetailView , UpdateView, DeleteView

from django.contrib.auth.views import LoginView

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Import the login_required decorator
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import date
import random

from main_app import forms 
from .forms import PracticeTestForm



from .models import (
    ShortAnswerQuestion,
    LongAnswerQuestion,
    MultipleChoiceQuestion,
    PracticeTest,
    UserResponse,
)

def home(request):
    return render(request, 'main_app/home.html')


# class CustomLoginView(LoginView):
#     template_name = 'login.html'
#     redirect_authenticated_user = True

def about(request):
    return render(request, 'main_app/about.html')

@login_required
def add_question(request):
    return render(request, 'main_app/addq.html')



def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect('question-index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
    # Same as: 
    # return render(
    #     request, 
    #     'signup.html',
    #     {'form': form, 'error_message': error_message}
    # )


def question_index(request):
    short_questions = ShortAnswerQuestion.objects.all()
    long_questions = LongAnswerQuestion.objects.all()
    mcq_questions = MultipleChoiceQuestion.objects.all()
    all_questions= list(short_questions)+list(long_questions)+list(mcq_questions) #turns query set into list
    random.shuffle(all_questions)

    context = {
        'short_questions': short_questions,
        'long_questions': long_questions,
        'mcq_questions': mcq_questions,
        'all_questions': all_questions,
    }

    return render(request, 'main_app/questions/index.html', context)

#short answer 
class ShortQuestionList(ListView):
    model = ShortAnswerQuestion
    context_object_name = 'shorts'
    template_name = 'main_app/short/short_list.html'

class ShortQuestionDetail(DetailView):
    model = ShortAnswerQuestion
    context_object_name = 'question'
    template_name = 'main_app/short/short_detail.html'

class ShortAnswerQuestionCreate(LoginRequiredMixin, CreateView):
    model = ShortAnswerQuestion
    fields = ['prompt', 'correct_answer'] 
    template_name = 'main_app/short/short_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user  #assign the logged-in user as the owner
        return super().form_valid(form)

class ShortAnswerQuestionUpdate(LoginRequiredMixin,UpdateView):
    model = ShortAnswerQuestion
    fields = ['prompt', 'correct_answer'] 
    template_name = 'main_app/short/short_form.html'

class ShortAnswerQuestionDelete(LoginRequiredMixin, DeleteView):
    model = ShortAnswerQuestion
    success_url = '/questions/short/'
    template_name = 'main_app/question_confirm_delete.html'


#long answer

class LongQuestionList(ListView):
    model = LongAnswerQuestion
    template_name = 'main_app/long/long_list.html'
    context_object_name = 'longs'

class LongQuestionDetail(DetailView):
    model = LongAnswerQuestion
    template_name = 'main_app/long/long_detail.html'
    context_object_name = 'question'

class LongAnswerQuestionCreate(LoginRequiredMixin, CreateView):
    model = LongAnswerQuestion
    fields = ['prompt', 'sample_answer']
    template_name = 'main_app/long/long_form.html'

    def form_valid(self, form): 
        form.instance.user = self.request.user 
        return super().form_valid(form)

class LongAnswerQuestionUpdate(LoginRequiredMixin, UpdateView):
    model = LongAnswerQuestion
    fields = ['prompt', 'sample_answer']
    template_name = 'main_app/long/long_form.html'


class LongAnswerQuestionDelete(LoginRequiredMixin, DeleteView):
    model = LongAnswerQuestion
    success_url = '/questions/long/'
    template_name = 'main_app/question_confirm_delete.html'


#multiple choice

class MCQList(ListView):
    model = MultipleChoiceQuestion
    context_object_name = 'mcqs'
    template_name = 'main_app/mcq/mcq_list.html'


class MCQDetail(DetailView):
    model = MultipleChoiceQuestion
    context_object_name = 'question'
    template_name = 'main_app/mcq/mcq_detail.html'

class MultipleChoiceQuestionCreate(LoginRequiredMixin, CreateView):
    model = MultipleChoiceQuestion
    fields = ['prompt', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']
    template_name = 'main_app/mcq/mcq_form.html'

    def form_valid(self, form): 
        form.instance.user = self.request.user 
        return super().form_valid(form)

class MultipleChoiceQuestionUpdate(LoginRequiredMixin, UpdateView):
    model = MultipleChoiceQuestion
    fields = ['prompt', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']
    template_name = 'main_app/mcq/mcq_form.html'

class MultipleChoiceQuestionDelete(LoginRequiredMixin, DeleteView):
    model = MultipleChoiceQuestion
    success_url = '/questions/mcq-questions/'
    template_name = 'main_app/question_confirm_delete.html'


# practice test views

def associate_question(request, practice_id, question_id, question_type):
    # Note that you can pass a question's id instead of the whole object
    # PracticeTest.objects.get(id=practice_id).questions.add(question_id)
    practice = PracticeTest.objects.get(id=practice_id)

    #if else statements, if question type is X, look at here in the database to find the question and associate it//long answer.objects//short answer.objects 
    if question_type =="short":
        question = ShortAnswerQuestion.objects.get(id=question_id)
    elif question_type=="long":
        question = LongAnswerQuestion.objects.get(id=question_id)
    elif question_type=="mcq":
        question = MultipleChoiceQuestion.objects.get(id=question_id)

    practice.questions.add(question)
    return redirect('practice-detail', practice_id=practice_id)



@login_required
def practiceTestDetail(request):
    mcq_questions = MultipleChoiceQuestion.objects.all()
    short_questions = ShortAnswerQuestion.objects.all()
    long_questions = LongAnswerQuestion.objects.all()
    return render(request, 'main_app/practice/practice_detail.html', {"mcq_questions":mcq_questions, "short_questions": short_questions, "long_questions": long_questions})


class CreatePracticeTest(LoginRequiredMixin, CreateView):
    model = PracticeTest
    fields = [ 'title', 'short_answer_questions', 'long_answer_questions', 'mcq_questions']   
    template_name = 'main_app/practice/practice_form.html'

    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the cat
        # Let the CreateView do its job as usual
        return super().form_valid(form) #this essentially interrupts the normal flow of the form submission to add the user before saving

class PracticeTestList(ListView):
    model = PracticeTest
    template_name = 'main_app/practice_test_list.html'  # you can customize
    context_object_name = 'practice_tests'  

class UpdatePracticeTest(LoginRequiredMixin, UpdateView):
    model = PracticeTest
    fields = ['title', 'short_answer_questions', 'long_answer_questions', 'mcq_questions']
    template_name = 'main_app/practice/practice_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeletePracticeTest(LoginRequiredMixin, DeleteView):
    model = PracticeTest
    template_name = 'main_app/practice/practice_confirm_delete.html'
    success_url = 'practice-test-index'

# class QuestionCreate(CreateView):
#     model = MultipleChoiceQuestion  # or ShortAnswerQuestion / LongAnswerQuestion
#     fields = ['prompt', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']
#     template_name = 'main_app/question_form.html'
#     success_url = '/questions/'

# class QuestionUpdate(UpdateView):
#     model = MultipleChoiceQuestion  # or ShortAnswerQuestion / LongAnswerQuestion
#     fields = ['prompt', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']
#     template_name = 'main_app/question_form.html'
#     success_url = '/questions/'

# class QuestionDelete(DeleteView):
#     model = MultipleChoiceQuestion  # or ShortAnswerQuestion / LongAnswerQuestion
#     success_url = '/questions/'
#     success_url = '/cards/'


# class MultipleChoiceQuestionForm(forms.ModelForm):
#     class Meta:
#         model = MultipleChoiceQuestion
#         fields = '__all__'

# class ShortAnswerQuestionForm(forms.ModelForm):
#     class Meta:
#         model = ShortAnswerQuestion
#         fields = '__all__'

# class LongAnswerQuestionForm(forms.ModelForm):
#     class Meta:
#         model = LongAnswerQuestion
#         fields = '__all__'
