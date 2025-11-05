import json
from django.core.management.base import BaseCommand
from main_app.models import MultipleChoiceQuestion

class Command(BaseCommand):
    help = "Import clean MTEL questions"

    def handle(self, *args, **kwargs):
        path = "practice/data/mtel_questions.json"
        with open(path, "r") as f:
            data = json.load(f)

        count = 0
        for item in data:
            prompt = item["prompt"].split("Option")[0].strip()
            choices = item["choices"]

            MultipleChoiceQuestion.objects.create(
                prompt=prompt[:2000],
                option_a=choices.get("A", "")[:255],
                option_b=choices.get("B", "")[:255],
                option_c=choices.get("C", "")[:255],
                option_d=choices.get("D", "")[:255],
                correct_answer=item.get("correct", "").strip()[:1]
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Imported {count} clean questions."))
