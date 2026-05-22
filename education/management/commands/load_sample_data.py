  
from django.core.management.base import BaseCommand
from education.models import Course, Module, Exam, Question

class Command(BaseCommand):
    help = 'Load sample courses, modules, and questions for testing'
    
    def handle(self, *args, **kwargs):
        self.stdout.write('Loading sample data...')
        
        tenth_course, created = Course.objects.get_or_create(
            level='10th',
            defaults={
                'title': '10th Foundation Course',
                'description': 'Complete foundation course for Class 10 students covering Math, Science, English, Social Science.',
                'duration_months': 3,
                'is_active': True,
            }
        )
        
        if created:
            modules_data = [
                {'title': 'Mathematics Basics', 'content': 'Algebra, Geometry, Statistics fundamentals', 'order': 1},
                {'title': 'Science Fundamentals', 'content': 'Physics, Chemistry, Biology core concepts', 'order': 2},
                {'title': 'English Grammar', 'content': 'Grammar rules, comprehension, writing skills', 'order': 3},
            ]
            
            for mod_data in modules_data:
                Module.objects.create(course=tenth_course, **mod_data)
            
            exam = Exam.objects.create(course=tenth_course, total_questions=5, passing_percentage=70.0)
            
            sample_questions = [
                {'question_text': 'What is 2 + 2?', 'option_a': '3', 'option_b': '4', 'option_c': '5', 'option_d': '6', 'correct_option': 'B'},
                {'question_text': 'Water boils at?', 'option_a': '90C', 'option_b': '100C', 'option_c': '110C', 'option_d': '120C', 'correct_option': 'B'},
                {'question_text': 'Past tense of go?', 'option_a': 'goed', 'option_b': 'went', 'option_c': 'goes', 'option_d': 'going', 'correct_option': 'B'},
                {'question_text': 'Capital of India?', 'option_a': 'Mumbai', 'option_b': 'Delhi', 'option_c': 'Kolkata', 'option_d': 'Chennai', 'correct_option': 'B'},
                {'question_text': 'H2O is?', 'option_a': 'Salt', 'option_b': 'Water', 'option_c': 'Sugar', 'option_d': 'Acid', 'correct_option': 'B'},
            ]
            
            for q_data in sample_questions:
                Question.objects.create(exam=exam, **q_data)
            
            self.stdout.write(self.style.SUCCESS('Sample 10th course created with modules and exam'))
        else:
            self.stdout.write('10th course already exists')
        
        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully'))