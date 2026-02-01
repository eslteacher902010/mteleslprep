import os
import django

# 1. Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mteleslprep.settings')
django.setup()

from main_app.models import PracticeTest, MultipleChoiceQuestion, User

def seed_data():
    # 2. Get the admin user
    admin = User.objects.filter(is_superuser=True).first()
    if not admin:
        admin = User.objects.first()

    # 3. Clean up existing data to avoid duplicates
    print("Wiping old tests and questions...")
    PracticeTest.objects.all().delete()
    MultipleChoiceQuestion.objects.all().delete()

    # 4. Create the Test Object
    test = PracticeTest.objects.create(
        title="MTEL ESL MCQ Simulation", 
        user=admin
    )

    # 5. Define the 15 questions
    questions_data = [
        {"p":"Which describes the 'Affective Filter'?","a":"Grammar tool","b":"Emotional barrier","c":"L1 interference","d":"Memory limit","ans":"B","ex":"Krashen's hypothesis on anxiety blocking input."},
        {"p":"Scaffolding is associated with which theorist?","a":"Chomsky","b":"Skinner","c":"Vygotsky","d":"Piaget","ans":"C","ex":"Linked to the Zone of Proximal Development."},
        {"p":"Smallest unit of meaning in a language?","a":"Phoneme","b":"Morpheme","c":"Syntax","d":"Lexicon","ans":"B","ex":"Morphemes carry meaning; phonemes are sounds."},
        {"p":"Student says 'I goed to the park.' This is:","a":"Code-switching","b":"Fossilization","c":"Overregularization","d":"Negative transfer","ans":"C","ex":"Applying regular rules to irregular verbs."},
        {"p":"Primary goal of SIOP (Sheltered Instruction)?","a":"Grammar drills","b":"Content + Language","c":"Translation","d":"Test exemption","ans":"B","ex":"Teaching content while developing English proficiency."},
        {"p":"Which court case ruled against 'sink or swim'?","a":"Brown v. Board","b":"Lau v. Nichols","c":"Plyler v. Doe","d":"Castañeda","ans":"B","ex":"Lau v. Nichols (1974) mandated help for ELLs."},
        {"p":"The difference between 'bit' and 'pit' is a:","a":"Morpheme","b":"Phoneme","c":"Grapheme","d":"Digraph","ans":"B","ex":"Phonemes distinguish word meanings."},
        {"p":"Assessment used during instruction?","a":"Summative","b":"Diagnostic","c":"Formative","d":"Standardized","ans":"C","ex":"Formative assessments inform ongoing teaching."},
        {"p":"BICS usually takes how long to develop?","a":"6 months","b":"1-2 years","c":"5-7 years","d":"Never","ans":"B","ex":"Social language develops relatively quickly."},
        {"p":"CALP usually takes how long to develop?","a":"1 year","b":"2-3 years","c":"5-7 years","d":"10 years","ans":"C","ex":"Academic language takes 5-7 years."},
        {"p":"What is 'Pragmatics'?","a":"Word order","b":"Sounds","c":"Social context","d":"Origins","ans":"C","ex":"Context contributes to meaning."},
        {"p":"A word with common origins in two languages?","a":"Homonym","b":"Antonym","c":"Cognate","d":"Slang","ans":"C","ex":"e.g., 'Information' and 'Información'."},
        {"p":"Teacher repeats error correctly without comment?","a":"Direct","b":"Recasting","c":"Elicitation","d":"Silence","ans":"B","ex":"Recasting provides implicit correction."},
        {"p":"Stage where students listen but don't speak?","a":"Emergence","b":"Fluency","c":"Pre-production","d":"Early Production","ans":"C","ex":"Known as the Silent Period."},
        {"p":"Law protecting school access for undocumented?","a":"Lau","b":"Plyler v. Doe","c":"NCLB","d":"ESSA","ans":"B","ex":"Plyler v. Doe (1982) ensures right to education."}
    ]

    # 6. Loop and save
    for item in questions_data:
        q = MultipleChoiceQuestion.objects.create(
            prompt=item['p'],
            option_a=item['a'],
            option_b=item['b'],
            option_c=item['c'],
            option_d=item['d'],
            correct_answer=item['ans'],
            explanation=item['ex'],
            user=admin
        )
        test.mcq_questions.add(q)

    print(f"Success! Test created with {test.mcq_questions.count()} questions.")

if __name__ == "__main__":
    seed_data()