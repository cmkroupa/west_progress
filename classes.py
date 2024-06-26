class Subject:
    def __init__(self,href:str, breadth:str, campuses:str):
        self._href = href
        self._breadth = breadth.split(" ")
        self._campuses = campuses.split(" ")
        self._courses = {}

class Course:
    def __init__(self,href):
        self._href = href
        self._name = ""
        self._code = ""
        self._description = ""
        self._anti_req = []
        self._pre_req = []
        self._extra = ""
    
    def add(self, course):
        if isinstance(course,Pre_Req):
            self._pre_req.append(course)
        elif isinstance(course, str):
            self._anti_req.append(course)
        else:
            raise TypeError("COURSE ADD ERROR")

class Pre_Req:
    def __init__(self, amount):
        self._amount = amount
        self._courses = []
    def addPreReq(self, course):
        if isinstance(course,Pre_Course):
            self._courses.append(course)
        else:
            raise TypeError("PREREQ ERROR")

class Pre_Course:
    def __init__(self, name, grade):
        self._name = name
        if(grade == 0):
            self._grade = 50
        else:
            self._grade = grade
    
    def name(self):
        return self._name
    def grade(self):
        return self._grade


