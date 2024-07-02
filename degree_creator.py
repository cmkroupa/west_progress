from creds import collection
from typing import List

from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()

    page.goto('https://westerncalendar.uwo.ca/faculties.cfm?SelectedCalendar=Live&ArchiveID=')

    faculties = {}

    rows = page.locator('tbody').locator('tr').all()

    for row in rows:
        columns = row.locator('td').all()
        a = columns[0].locator('a')

        href = a.get_attribute("href")
        faculty = a.inner_text().strip()

        faculties[faculty] = {"href": ("https://westerncalendar.uwo.ca/"+href)}
    
    
    for faculty in faculties:
        page.goto(faculties[faculty]['href'])
        page.click('a[href=\\#collapsePrograms]')
        page.wait_for_selector('div.moduleDept')
        modules = page.locator('div.moduleDept').all()
        for module in modules:
            href = module.locator('a').get_attribute('href')
            inner = module.locator('a').inner_text()
            faculties[faculty][inner] = {"href": ("https://westerncalendar.uwo.ca/"+href)}
    
    for faculty in faculties:
        for module in faculties[faculty]:
            page.goto(faculties[faculty][module][href])
            moduleSection = page.locator('div.moduleInfo')
        


