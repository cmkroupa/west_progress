from creds import collection
from classes import *
from typing import List

from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    page.goto("https://westerncalendar.uwo.ca/Courses.cfm?SelectedCalendar=Live&ArchiveID=")

    page_subjects = page.locator('tbody').locator('tr').all()

    subjects: List[Subject] = {}

    for page_subject in page_subjects:
        columns = page_subject.locator('td').all()
        subjectName = columns[0].locator('a').inner_text()
        subjectHREF = columns[0].locator('a').get_attribute('href')

        breadthText = columns[1].inner_text()
        breadth = []
        if("CATEGORY A" in breadthText):
            breadth.append("A")
        if("CATEGORY B" in breadthText):
            breadth.append("B")
        if("CATEGORY C" in breadthText):
            breadth.append("C")

        locations = []
        divs = columns[2].locator('div').all()
        for div in divs:
            src = div.locator('img').get_attribute('src')
            if("westernIcon" in src):
                locations.append('Western')
            elif("kingsicon" in src):
                locations.append('Kings')
            else:
                locations.append('Huron')
        
        subjects[subjectName] = Subject("https://westerncalendar.uwo.ca/"+subjectHREF, breadth, locations)
    for subject in subjects:
        courses = []
        
        page.goto(subjects[subject]._href) 
        page_courses = page.locator('div[class=panel-body]').filter(has=page.locator('a').filter(has_text="More details")).all()
        
        for page_course in page_courses:
            detailsButton = page_course.locator('a').filter(has_text="More details").get_attribute('href')
            courses.append("https://westerncalendar.uwo.ca/"+detailsButton)
                
        
        for course_page in courses:
            page.goto(course_page)
            body = page.locator('div#CourseInformationDiv')

            code = body.locator('h2').inner_text()
            name = body.locator('h3').inner_text()

            sections = body.locator('div.col-xs-12').all()
            description = sections[0].locator('div').inner_text()
            extra = sections[len(sections)-2].locator('div').inner_text()
            anti_req = []

            print(code)
            print("ANTI-REQ")
            while((anti_req_course := input("- ")) != ""):
                anti_req.append(anti_req_course)
            pre_req = []
            print("PRE-REQ")
            for i in range(0,int(input("How many sections: "))):
                pre_req_section = []
                weight = input('Weight: ')
                print("Section "+i+": ")
                while((pre_req_course := input("- ")) != ""):
                    grade = input('Grade Needed: ')
                    newCourse = Pre_Course(pre_req_course, grade)
                    pre_req_section.append(newCourse)
                pre_req.append(Pre_Req(weight, pre_req_section))

            courseToAdd = Course(name,course_page, description, anti_req, pre_req, extra)

            icon = body.locator('img').all()[0].get_attribute('alt')

            if("Western" in icon):
                icon = "Western"
            elif("King" in icon):
                icon = "Kings"
            else:
                icon = "Huron"

            if(code not in subjects):
                subjects[code] = {}
            
            subjects[code][icon] = courseToAdd


