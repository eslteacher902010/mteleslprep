from modulefinder import test
from django.contrib import messages
from urllib import request
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse


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
from .forms import PracticeTestForm, ShortAnswerQuestionForm, LongAnswerQuestionForm, MultipleChoiceQuestionForm



from .models import (
    ShortAnswerQuestion,
    LongAnswerQuestion,
    MultipleChoiceQuestion,
    PracticeTest,
    UserResponse,
    UserAttempt
)

def home(request):
    return render(request, 'main_app/home.html')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html' 
    redirect_authenticated_user = True

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

    def get_queryset(self):
        return ShortAnswerQuestion.objects.filter(user=self.request.user)

class ShortAnswerQuestionDelete(LoginRequiredMixin, DeleteView):
    model = ShortAnswerQuestion
    success_url = '/questions/short/'
    template_name = 'main_app/question_confirm_delete.html'

    def get_queryset(self):
        return ShortAnswerQuestion.objects.filter(user=self.request.user)



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

    def get_queryset(self):
        return LongAnswerQuestion.objects.filter(user=self.request.user)


class LongAnswerQuestionDelete(LoginRequiredMixin, DeleteView):
    model = LongAnswerQuestion
    success_url = '/questions/long/'
    template_name = 'main_app/question_confirm_delete.html'

    def get_queryset(self):
        return LongAnswerQuestion.objects.filter(user=self.request.user)    


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
    form_class = MultipleChoiceQuestionForm 
    template_name = 'main_app/mcq/mcq_form.html'

    def form_valid(self, form): 
        form.instance.user = self.request.user 
        return super().form_valid(form)

class MultipleChoiceQuestionUpdate(LoginRequiredMixin, UpdateView):
    model = MultipleChoiceQuestion
    form_class = MultipleChoiceQuestionForm
    template_name = 'main_app/mcq/mcq_form.html'

    def get_queryset(self):
        return MultipleChoiceQuestion.objects.filter(user=self.request.user)

class MultipleChoiceQuestionDelete(LoginRequiredMixin, DeleteView):
    model = MultipleChoiceQuestion
    success_url = '/questions/mcq-questions/'
    template_name = 'main_app/question_confirm_delete.html'

    def get_queryset(self):
        return MultipleChoiceQuestion.objects.filter(user=self.request.user)


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


# @login_required
def practice_test_detail(request, pk):
    practice_test = PracticeTest.objects.get(id=pk)


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mcq_questions'] = MultipleChoiceQuestion.objects.filter(user=self.request.user)
        context['short_questions'] = ShortAnswerQuestion.objects.filter(user=self.request.user)
        context['long_questions'] = LongAnswerQuestion.objects.filter(user=self.request.user)
        context['mcq_form'] = MultipleChoiceQuestionForm()
        context['short_form'] = ShortAnswerQuestionForm()
        context['long_form'] = LongAnswerQuestionForm()

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
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



def take_practice_test(request, practice_test_id):
    practice_test = get_object_or_404(PracticeTest, id=practice_test_id)

    # Track attempts only if logged in
    attempt = None
    attempt_number = 1
    if request.user.is_authenticated:
        attempt_count = UserAttempt.objects.filter(user=request.user, test=practice_test).count()
        attempt_number = attempt_count + 1
        attempt = UserAttempt.objects.create(
            user=request.user,
            test=practice_test,
            attempt_number=attempt_number
        )

    # 1. Fetch all questions
    mcq_qs = practice_test.mcq_questions.all()
    short_qs = practice_test.short_answer_questions.all()
    long_qs = practice_test.long_answer_questions.all()

    # 2. Combine into a single list for the template loop
    # We convert querysets to lists to concatenate them easily
    all_questions = list(mcq_qs) + list(short_qs) + list(long_qs)
    total_questions = len(all_questions)

    # ---- GET: show the test ----
    if request.method == "GET":
        return render(request, 'main_app/practice/take_practice_test.html', {
            'practice_test': practice_test,
            'all_questions': all_questions, # Use this single list in your HTML loop
            'total_questions': total_questions,
            'attempt_number': attempt_number,
        })

    # ---- POST: grade the test ----
    score = 0
    total_mcqs = 0

    # Logic to process POST data
    # ---- POST: grade the test ----
    score = 0
    total_mcqs = 0

    for q in all_questions:
        # Check all possible naming conventions from your HTML
        # We check for mcq_question_ID, short_question_ID, etc.
        user_answer = (
            request.POST.get(f'mcq_question_{q.id}') or 
            request.POST.get(f'short_question_{q.id}') or 
            request.POST.get(f'long_question_{q.id}', '')
        ).strip()
        
        # Use hasattr to check the specific model type
        is_mcq = hasattr(q, 'option_a')
        is_correct = False

        if is_mcq:
            total_mcqs += 1
            if user_answer.lower() == q.correct_answer.lower():
                score += 1
                is_correct = True
        
        # Logic for auto-grading short answer (optional)
        elif hasattr(q, 'correct_answer'): # This is a ShortAnswerQuestion
             if user_answer.lower() == q.correct_answer.lower():
                is_correct = True

        if request.user.is_authenticated:
            UserResponse.objects.create(
                user=request.user,
                test=practice_test,
                question_type=getattr(q, 'question_type', 'unknown'),
                question_id=q.id,
                question_text=q.prompt,
                user_answer=user_answer,
                is_correct=is_correct,
                attempt=attempt,
                # Safe way to get correct answer regardless of model
                correct_answer=getattr(q, "correct_answer", getattr(q, "sample_answer", "")),
            )

    if request.user.is_authenticated and attempt:
        attempt.score = score
        attempt.save()

    return redirect('practice-results', practice_test_id=practice_test_id)



@login_required
def practice_results(request, practice_test_id):
    practice_test = get_object_or_404(PracticeTest, id=practice_test_id)
    responses = UserResponse.objects.filter(test=practice_test, user=request.user)

   
    score = responses.filter(is_correct=True).count()
    total = responses.filter(question_type='mcq').count()
    percentage = round((score / total * 100), 1) if total else 0

    latest_attempt= (
        UserAttempt.objects.filter(user=request.user, test=practice_test)
        .order_by('-started_at')
        .first()
    )
    responses = UserResponse.objects.filter(attempt=latest_attempt)


    return render(request, "main_app/practice/results.html", {
        "practice_test": practice_test,
        "responses": responses,
        "score": score,
        "total": total,
        "percentage": percentage,
        "latest_attempt":latest_attempt,
    })


def next_question(request, test_id, q_num):
    #fetch practice test 
    practice_test = get_object_or_404(PracticeTest, id=test_id)
    
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        selected_choice = request.POST.get('answer')

        if question_id and selected_choice:
            UserResponse.objects.create(
                user=request.user,
                test=practice_test,
                question_id=question_id,
                user_answer=selected_choice,
            )

    all_questions = (
        list(practice_test.mcq_questions.all()) +
        list(practice_test.short_answer_questions.all()) +
        list(practice_test.long_answer_questions.all())
    )

    total = len(all_questions)
    
    if q_num > total:
        return JsonResponse({'done': True})

    question = all_questions[q_num - 1] #Current questions

    data = {
        'done': False,
        'q_num': q_num,
        'total': total,
        'question': {
            'id': question.id,
            'prompt': question.prompt,
            'type': question.__class__.__name__,
        }
    }

    if hasattr(question, 'option_a'):
        data['question']['choices'] = [
            {'label': 'A', 'text': question.option_a},
            {'label': 'B', 'text': question.option_b},
            {'label': 'C', 'text': question.option_c},
            {'label': 'D', 'text': question.option_d},
        ]

    return JsonResponse(data)



def check_answer(request, question_id):
    # Get the type from the URL parameters
    q_type = request.GET.get('type') 
    
    if q_type == 'mcq':
        question = get_object_or_404(MultipleChoiceQuestion, id=question_id)
        selected = request.GET.get('choice', '').strip().upper()
        correct = question.correct_answer.upper()
        return JsonResponse({
            "is_correct": selected == correct,
            "correct_answer": correct,
            "explanation": question.explanation or "No explanation provided."
        })
    
    # Handle Short/Long Answer separately
    model = ShortAnswerQuestion if q_type == 'short' else LongAnswerQuestion
    question = get_object_or_404(model, id=question_id)
    return JsonResponse({
        "correct_answer": getattr(question, 'correct_answer', getattr(question, 'sample_answer', '')),
        "explanation": "Compare your response to the sample provided."
    })
