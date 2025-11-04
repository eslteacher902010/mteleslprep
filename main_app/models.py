from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


#add a helper for all data of all questions 
# Short Answer Question
class ShortAnswerQuestion(models.Model):
    prompt = models.TextField()
    question_type= "short"
    correct_answer = models.TextField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f"Short: {self.prompt[:50]}"
    
    def get_absolute_url(self):
        return reverse('short-detail', kwargs={'pk': self.id})


# Long Answer Question
class LongAnswerQuestion(models.Model):
    prompt = models.TextField()
    question_type= "long"
    sample_answer = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Long: {self.prompt[:50]}"
    
    def get_absolute_url(self):
        return reverse('long-detail', kwargs={'pk': self.id})



# Multiple Choice Question
class MultipleChoiceQuestion(models.Model):
    prompt = models.TextField()
    question_type="mcq"
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    correct_answer = models.CharField(max_length=1, choices=[
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]) 

    def __str__(self):
        return f"MCQ: {self.prompt[:50]}"
    
    def get_absolute_url(self):
        return reverse('mcq-detail', kwargs={'pk': self.id})



# Practice test session
class PracticeTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="practice_tests")
    title = models.CharField(max_length=200, default="Untitled Test")
    date_taken = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(default=0)
    short_answer_questions = models.ManyToManyField(ShortAnswerQuestion, blank=True)
    long_answer_questions = models.ManyToManyField(LongAnswerQuestion, blank=True)
    mcq_questions = models.ManyToManyField(MultipleChoiceQuestion, blank=True)


    def __str__(self):
        return f"{self.user.username} - {self.date_taken.strftime('%Y-%m-%d %H:%M')}"
    
    def get_absolute_url(self):
        return reverse('practice-detail', kwargs={'pk': self.id})

class UserAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(PracticeTest, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(default=0)
    attempt_number=models.IntegerField(default=0)
 
    def __str__(self):
        return f"{self.user.username} - {self.test.title} (Attempt {self.attempt_number})"


# Individual user responses
class UserResponse(models.Model):
    test = models.ForeignKey(PracticeTest, on_delete=models.CASCADE, related_name="responses")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(
        max_length=20,
        choices=[
            ('short', 'Short Answer'),
            ('long', 'Long Answer'),
            ('mcq', 'Multiple Choice'),
        ]
    )
    question_id = models.PositiveIntegerField()  # the specific question’s ID
    user_answer = models.TextField(blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    attempt = models.ForeignKey(UserAttempt, on_delete=models.CASCADE, null=True, blank=True)
    correct_answer = models.CharField(max_length=255, blank=True, null=True)



    def __str__(self):
        return f"Response by {self.user.username} ({self.question_type})"

