from django import forms
from .models import PracticeTest, ShortAnswerQuestion, LongAnswerQuestion, MultipleChoiceQuestion



class ShortAnswerQuestionForm(forms.ModelForm):
    class Meta:
        model = ShortAnswerQuestion
        fields = ['prompt', 'correct_answer']
        widgets = {
            'prompt': forms.Textarea(attrs={'rows': 3}),
            'answer': forms.Textarea(attrs={'rows': 3}),
        }

class LongAnswerQuestionForm(forms.ModelForm):
    class Meta:
        model = LongAnswerQuestion
        fields = ['prompt', 'sample_answer']
        widgets = {
            'prompt': forms.Textarea(attrs={'rows': 3}),
            'answer': forms.Textarea(attrs={'rows': 3}),
        }

class MultipleChoiceQuestionForm(forms.ModelForm):
    class Meta:
        model = MultipleChoiceQuestion
        fields = ['prompt', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']
        widgets = {
            'prompt': forms.Textarea(attrs={'rows': 3}),
            'option_a': forms.TextInput(),
            'option_b': forms.TextInput(),
            'option_c': forms.TextInput(),
            'option_d': forms.TextInput(),
            'correct_answer': forms.Select(),
        }


class PracticeTestForm(forms.ModelForm):
    class Meta:
        model = PracticeTest
        fields = ['title', 'short_answer_questions', 'long_answer_questions', 'mcq_questions']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter a descriptive title'}),
            'short_answer_questions': forms.CheckboxSelectMultiple(),
            'long_answer_questions': forms.CheckboxSelectMultiple(),
            'mcq_questions': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['short_answer_questions'].queryset = ShortAnswerQuestion.objects.filter(user=user)
            self.fields['long_answer_questions'].queryset = LongAnswerQuestion.objects.filter(user=user)
            self.fields['mcq_questions'].queryset = MultipleChoiceQuestion.objects.filter(user=user)