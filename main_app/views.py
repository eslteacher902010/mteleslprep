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
        practice.short_answer_questions.add(question)

    elif question_type=="long":
        question = LongAnswerQuestion.objects.get(id=question_id)
        practice.long_answer_questions.add(question)
    elif question_type=="mcq":
        question = MultipleChoiceQuestion.objects.get(id=question_id)
        practice.mcq_questions.add(question)

    return redirect('practice-detail', pk=practice_id)


@login_required
def practice_test_detail(request, practice_id):
    # Get the selected PracticeTest
    practice_test = PracticeTest.objects.get(id=practice_id)

    # Example: show only questions not yet associated (if applicable)
    mcq_questions = practice_test.mcq_questions.all()
    short_questions = practice_test.short_answer_questions.all()
    long_questions = practice_test.long_answer_questions.all()

    return render(request, 'main_app/practice/practice_detail.html', {
        'practice_test': practice_test,
        'mcq_questions': mcq_questions,
        'short_questions': short_questions,
        'long_questions': long_questions,
    })


class CreatePracticeTest(LoginRequiredMixin, CreateView):
    model = PracticeTest
    form_class = PracticeTestForm
    template_name = 'main_app/practice/practice_form.html'



    def form_valid(self, form):
        # Assign the logged-in user
        form.instance.user = self.request.user
        # Continue with the normal save/redirect process
        return super().form_valid(form)



class PracticeTestList(ListView):
    model = PracticeTest
    template_name = 'main_app/practice/practice_list.html'  
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
    success_url = '/practice-tests/'



def associate_question(request, practice_id, question_id, question_type):
    practice = PracticeTest.objects.get(id=practice_id)
    #collect all the practice test objects
    if question_type =="short":
        question = ShortAnswerQuestion.objects.get(id=question_id)
        practice.short_answer_questions.add(question)

    elif question_type=="long":
        question = LongAnswerQuestion.objects.get(id=question_id)
        practice.long_answer_questions.add(question)
    elif question_type=="mcq":
        question = MultipleChoiceQuestion.objects.get(id=question_id)
        practice.mcq_questions.add(question)


    return redirect('practice-detail', pk=practice_id)

#not finished
@login_required
def take_practice_test(request, practice_test_id):
    practice_test = get_object_or_404(PracticeTest, id=practice_test_id)

    mcq_questions = practice_test.mcq_questions.all()
    short_questions = practice_test.short_answer_questions.all()
    long_questions = practice_test.long_answer_questions.all()

    if request.method == "GET":
        return render(request, 'main_app/practice/take_practice_test.html', {
            'practice_test': practice_test,
            'mcq_questions': mcq_questions,
            'short_questions': short_questions,
            'long_questions': long_questions,
        })

    score = 0
    total = 0

    test_questions = {
        'mcq': mcq_questions,
        'short': short_questions,
        'long': long_questions
    }

    for q_type, questions in test_questions.items():
        for q in questions:
            user_answer = request.POST.get(f'{q_type}_question_{q.id}', '').strip()
            is_correct = False

            if q_type == 'mcq':
                total += 1
                if user_answer.lower() == q.correct_answer.lower():
                    score += 1
                    is_correct = True

            UserResponse.objects.create(
                user=request.user,
                test=practice_test,
                question_type=q_type,
                question_id=q.id,
                question_text=q.prompt,
                user_answer=user_answer,
                is_correct=is_correct
            )

    percentage = round((score / total * 100), 1) if total else 0
    practice_test.score = score
    practice_test.save()

    return redirect('practice-results', practice_test_id=practice_test_id)



@login_required
def practice_results(request, practice_test_id):
    practice_test = get_object_or_404(PracticeTest, id=practice_test_id)
    responses = UserResponse.objects.filter(test=practice_test, user=request.user)

    score = responses.filter(is_correct=True).count()
    total = responses.filter(question_type='mcq').count()
    percentage = round((score / total * 100), 1) if total else 0

    return render(request, "main_app/practice/results.html", {
        "practice_test": practice_test,
        "responses": responses,
        "score": score,
        "total": total,
        "percentage": percentage
    })






