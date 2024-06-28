from creds import collection
from typing import List

from playwright.sync_api import sync_playwright

done = ["Actuarial Science","American Sign Language","American Studies","Analytics and Decision Sciences","Anatomy and Cell Biology"]

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    page.goto("https://westerncalendar.uwo.ca/Courses.cfm?SelectedCalendar=Live&ArchiveID=")

    page_subjects = page.locator('tbody').locator('tr').all()

    subjects = {}

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
        
        subjects[subjectName] = {"href":"https://westerncalendar.uwo.ca/"+subjectHREF, "breadth": breadth,"campuses": locations}

    for subject in subjects:
        print(subject)
        if(subject in done):
            print("skipped")
            continue

        subjects[subject]['courses'] = {}
        courses = []
        
        page.goto(subjects[subject]["href"]) 
        page_courses = page.locator('div[class=panel-body]').filter(has=page.locator('a').filter(has_text="More details")).all()
        
        for page_course in page_courses:
            detailsButton = page_course.locator('a').filter(has_text="More details").get_attribute('href')
            courses.append("https://westerncalendar.uwo.ca/"+detailsButton)
            
        #referencing courses  
        for course_page in courses:
            page.goto(course_page)

            input()
            continue
            body = page.locator('div#CourseInformationDiv')

            code = body.locator('h2').inner_text()
            name = body.locator('h3').inner_text()

            sections = body.locator('div.col-xs-12').all()
            description = sections[0].locator('div').inner_text()
            extra = sections[len(sections)-2].locator('div').inner_text().replace('Extra Information: ', "")

            courseToAdd = {
                "name": name,
                "href":course_page,
                "description":description,
                "extra":extra
            }

            icon = body.locator('img').all()[0].get_attribute('alt')

            if("Western" in icon):
                icon = "Western"
            elif("King" in icon):
                icon = "Kings"
            else:
                icon = "Huron"

            if(code not in subjects[subject]['courses']):
                subjects[subject]['courses'][code] = {}
            
            subjects[subject]['courses'][code][icon] = courseToAdd

            anti_req = []
            anti_s = body.locator('div.col-xs-12').filter(has_text="Antirequisite").locator('a').all()
            if(len(anti_s) > 0):
                for anti in anti_s:
                    anti_req.append(anti.inner_text().replace(",",""))
                subjects[subject]['courses'][code][icon]['anti_req'] = anti_req
            
            
            pre_s = body.locator('div.col-xs-12').filter(has_text="Prerequisite").locator('a').all()
            if(len(pre_s) > 0):
                pre_dict = {}
                pre_dict["section1"] = {}

                pre_dict["section1"]["weight"] = 0.5
                pre_dict["section1"]["courses"] = {}

                for pre in pre_s:
                    pre_dict["section1"]["courses"][pre.inner_text().replace(",", "")] = 50
                
                subjects[subject]['courses'][code][icon]['pre_req'] = pre_dict
        
        #collection.insert_one({subject: subjects[subject]})


