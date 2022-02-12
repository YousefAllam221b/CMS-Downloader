import requests
from requests_ntlm import HttpNtlmAuth
import bs4 as bs

# Making a get request
Home_Page_Response = requests.get('https://cms.guc.edu.eg/apps/student/HomePageStn.aspx',
            auth = HttpNtlmAuth('yousef.alam', 'JohnWatson123!')).text

Home_Page_Html = bs.BeautifulSoup(Home_Page_Response, 'html.parser')
Html_Files = []
# Getting Courses info Courses table
tableID = 'ContentPlaceHolderright_ContentPlaceHoldercontent_GridViewcourses'
CoursesNames = Home_Page_Html.select(tableID + ' td:nth-child(2)')
CoursesIDs = Home_Page_Html.select(tableID + ' td:nth-child(5)')
StudentIDs = Home_Page_Html.select(tableID + ' td:nth-child(6)')

for i in range(len(CoursesNames)):
    CourseDict = {'Name': CoursesNames[i].getText(), 'ID': CoursesIDs[i].getText(), 'SID': StudentIDs[i].getText()}
    Html_Files.append(CourseDict)
