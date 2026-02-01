import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mteleslprep.settings')
django.setup()

from main_app.models import PracticeTest, MultipleChoiceQuestion, User

def add_literacy_test():
    admin = User.objects.filter(is_superuser=True).first() or User.objects.first()
    
    # Create the new test object
    test = PracticeTest.objects.create(
        title="ESL Literacy & Methods Simulation", 
        user=admin
    )

    questions = [
        {"p":"Which strategy best supports 'Top-Down' reading processing?","a":"Phonics drills","b":"Predicting based on title","c":"Identifying phonemes","d":"Memorizing sight words","ans":"B","ex":"Top-down uses prior knowledge and context."},
        {"p":"What is 'Automaticity' in reading?","a":"Reading with expression","b":"Decoding without conscious effort","c":"Understanding metaphors","d":"Summarizing a text","ans":"B","ex":"Automaticity is fast, effortless word recognition."},
        {"p":"Total Physical Response (TPR) is most effective for:","a":"Advanced academic writing","b":"Beginning language learners","c":"Learning complex grammar","d":"Standardized test prep","ans":"B","ex":"TPR uses physical movement to react to input."},
        {"p":"A student reads 'The dog ran' as 'The dig ran.' This is an error in:","a":"Semantics","b":"Syntax","c":"Graphophonics","d":"Pragmatics","ans":"C","ex":"Graphophonics relates to letter-sound relationships."},
        {"p":"Which best describes the 'Language Experience Approach' (LEA)?","a":"Using student-dictated stories as text","b":"Strictly following a basal reader","c":"Focusing only on silent reading","d":"Translating texts from L1 to L2","ans":"A","ex":"LEA uses students' own words to build literacy."},
        {"p":"What is the 'Matthew Effect' in reading?","a":"The impact of phonics on fluency","b":"The widening gap between slow and fast readers","c":"The benefit of bilingualism","d":"The stages of spelling development","ans":"B","ex":"Strong readers get stronger while weak readers fall behind."},
        {"p":"Which is an example of an 'Authentic Assessment'?","a":"Multiple-choice grammar quiz","b":"Standardized state exam","c":"Student portfolio of writing projects","d":"Spelling bee","ans":"C","ex":"Authentic tasks reflect real-world application."},
        {"p":"What is 'Cloze' procedure?","a":"Reading a text backward","b":"Filling in missing words in a passage","c":"Repeating a teacher's sentences","d":"Timed silent reading","ans":"B","ex":"Cloze tests measure comprehension and vocabulary usage."},
        {"p":"The 'Natural Approach' (Krashen/Terrell) emphasizes:","a":"Error correction","b":"Grammar translation","c":"Communication and low anxiety","d":"Rote memorization","ans":"C","ex":"It mimics natural L1 acquisition."},
        {"p":"What are 'Realia'?","a":"Textbooks","b":"Digital flashcards","c":"Real-life objects used as props","d":"Practice worksheets","ans":"C","ex":"Realia provide concrete visual context for vocabulary."}
    ]

    for item in questions:
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

    print(f"Success! Added '{test.title}' with {test.mcq_questions.count()} questions.")

if __name__ == "__main__":
    add_literacy_test()