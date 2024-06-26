class Subject:
    def __init__(self,href:str, breadth:str, campuses:str):
        
        self._href = href
        self._breadth = breadth
        self._campuses = campuses
        self._courses = {}
    def getHREF(self):
        return self._href
    def getBreadth(self):
        return self._breadth
    def getCampuses(self):
        return self._campuses
    
    def addCourse(self,courseName):
        self._courses[courseName] = {}
    def getCourse(self, course):
        if(course in self._courses):
            return self._courses[course]
        return ""
    

class Course:
    def __init__(self,name, href, description, anti_req, pre_req, extra):
        self._href = href
        self._name = name
        self._description = description
        self._anti_req = anti_req
        self._pre_req = pre_req
        self._extra = extra.replace("Extra Information: ", "")
        
    def __str__(self):
        return "Name: "+self._name+"\nDescription: "+self._description+"\nExtra: "+self._extra

class Pre_Req:
    def __init__(self, amount, courses):
        self._amount = amount
        self._courses = courses

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


