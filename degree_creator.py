from creds import collection
from typing import List

from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
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


    


