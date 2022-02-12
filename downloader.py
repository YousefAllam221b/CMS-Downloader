import requests
from requests_ntlm import HttpNtlmAuth
import bs4 as bs
path = r'C:\Users\Youse\Documents\Semseter 6'

# Making a get request
def getRequest(path):
    recieve = requests.get(path, auth = HttpNtlmAuth('yousef.alam', 'JohnWatson123!'))
    return recieve.text

def downloadFiles(name, exe):
        with open(name + '.' + exe,'wb') as f:
            f.write(recieve.content)
def getCoursesInfoDict():
    Home_Page_Response = getRequest('https://cms.guc.edu.eg/apps/student/HomePageStn.aspx')
    Home_Page_Html = bs.BeautifulSoup(Home_Page_Response, 'html.parser')
    Html_Files = []
    # Getting Courses info Courses table
    tableID = '#ContentPlaceHolderright_ContentPlaceHoldercontent_GridViewcourses'
    CoursesNames = Home_Page_Html.select(tableID + ' td:nth-child(2)')
    CoursesIDs = Home_Page_Html.select(tableID + ' td:nth-child(5)')
    StudentIDs = Home_Page_Html.select(tableID + ' td:nth-child(6)')
    for i in range(len(CoursesNames)):
        CourseDict = {'Name': CoursesNames[i].getText(), 'ID': CoursesIDs[i].getText(), 'SID': StudentIDs[i].getText()}
        Html_Files.append(CourseDict)
    return Html_Files
