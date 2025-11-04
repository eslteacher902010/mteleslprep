from django.core.management.base import BaseCommand
from main_app.models import MultipleChoiceQuestion
import json
import os

class Command(BaseCommand):
    help = "Import MTEL multiple choice questions from JSON"

    def handle(self, *args, **kwargs):
        path = os.path.join("practice", "data", "mtel_questions.json")

        with open(path, "r") as f:
            questions = json.load(f)

        created = 0
        for q in questions:
            MultipleChoiceQuestion.objects.create(
    prompt=q["prompt"],
    option_a=q["choices"]["A"],
    option_b=q["choices"]["B"],
    option_c=q["choices"]["C"],
    option_d=q["choices"]["D"],
    correct_answer=q["correct"],  # your model uses this name
)

            created += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Imported {created} MTEL questions!"))
