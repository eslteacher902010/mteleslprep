from django.contrib import admin
from .models import (
    ShortAnswerQuestion,
    LongAnswerQuestion,
    MultipleChoiceQuestion,
    PracticeTest,
    UserResponse,
)

admin.site.register(ShortAnswerQuestion)
admin.site.register(LongAnswerQuestion)
admin.site.register(MultipleChoiceQuestion)
# admin.site.register(PracticeTest)
admin.site.register(UserResponse)

class PracticeTestAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_taken', 'score')
    filter_horizontal = ('short_answer_questions', 'long_answer_questions', 'mcq_questions')


admin.site.register(PracticeTest, PracticeTestAdmin)