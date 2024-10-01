from datetime import date
from main.server import ResultAPI, Parser
from main.models import  SGPA, Student, VTUResult, Semester, Subject, Result

class ResultManager:
    def __init__(self, usn=None, code=None) -> None:
        self.usn = usn
        self.vturesult = VTUResult.objects.get(code=code) 
        self.result_code = code
        self.result = ResultAPI(self.result_code)
        self.subjects = []
        self.student = None

    def from_database(self):
        self.student = Student.objects.get(usn=self.usn)
        self.subjects = Result.objects.filter(student=self.student, vturesult=self.vturesult).select_related('subject','semester').order_by("semester")
        if self.subjects.exists():
            return  self.student, self.subjects
        else:
            raise Exception("Student Result Not Found")
        
    def extract_college_and_branch(self, usn: str):
        if len(usn) != 10:
            raise ValueError("Invalid USN format")
        college_code = usn[1:3]  # Characters at positions 1 and 2
        branch_code = usn[5:7]   # Characters at positions 5 and 6
        return college_code, branch_code

    def get_captcha_token(self):
        return self.result.get_page(), self.result.cookies.get('VISRE')
    
    def from_vtu(self, token, captcha, cookies):
        content = self.result.get_result(token, captcha, self.usn, cookies)
        self.subjects = []
        if content:
            parser = Parser(content)
            student_info = parser.get_student_info()
            if student_info is None:
                raise Exception("Student Result Not Found")
            college_code, branch_code = self.extract_college_and_branch(student_info.usn)
            self.student, _ = Student.objects.get_or_create(usn=student_info.usn, name=student_info.name, defaults={"branch":branch_code})
            
            for subject in parser.get_subjects():
                semester, _ = Semester.objects.get_or_create(semester=subject.sem)
                subject_obj, _ = Subject.objects.get_or_create(code=subject.code,
                                                               defaults={'name': subject.name, 'sem': semester})
                _result = Result(
                    student=self.student,
                    semester=semester,
                    vturesult=self.vturesult,
                    internal=subject.internal,
                    external=subject.external,
                    total=subject.total,
                    result=subject.result,
                    subject=subject_obj,
                )
                self.subjects.append(_result)
                Result.objects.bulk_create(self.subjects, ignore_conflicts=True, unique_fields=('student', 'vturesult', 'subject'))
            
            self.save_result_data()
            return self.student, self.subjects
            
        else:
            raise Exception("Student Result Not Found")

    def get_result(self) -> tuple[bool, dict]:
        try:
            return True, self.from_database()
        except:
            token, cookie_value = self.get_captcha_token()
            return False, {'token': token, 'cookie_value': cookie_value}

    def get_sgpa(self):
        total_credits = total_numerical = 0
        for sub in self.subjects:
            if sub.subject.credits is None:
                return None  
            total_credits += sub.subject.credits
            total_numerical += sub.subject.credits * self.marks_to_grade(sub.total)
        if total_credits == 0:  # Prevent division by zero
            return None
        return round(total_numerical / total_credits, 2)

    
    @staticmethod
    def marks_to_grade(marks):
        try:
            marks = int(marks)
        except ValueError:
            return 0
        if 100 >= marks >= 90:
            return 10
        elif 89 >= marks >= 80:
            return 9
        elif 79 >= marks >= 70:
            return 8
        elif 69 >= marks >= 60:
            return 7
        elif 59 >= marks >= 55:
            return 6
        elif 54 >= marks >= 50:
            return 5
        elif 49 >= marks >= 40:
            return 4
        elif 39 >= marks >= 0:
            return 0
        else:
            return 0
        
    def save_result_data(self):
        SGPA.objects.get_or_create(
            student = self.student,
            result = self.vturesult,
            defaults=dict(
                sgpa = self.get_sgpa(),
                semester = self.subjects[0].semester
            )
        )
