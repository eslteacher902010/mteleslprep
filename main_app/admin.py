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
admin.site.register(PracticeTest)
admin.site.register(UserResponse)
