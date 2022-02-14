import requests
from requests_ntlm import HttpNtlmAuth
import bs4 as bs
import re
import os
mainDir = r'C:\Users\Youse\Documents\Semester 6'
os.chdir(mainDir    )
# Making a get request
def getRequest(path):
    recieve = requests.get(path, auth = HttpNtlmAuth('yousef.alam', 'JohnWatson123!'))
    return recieve

def getCoursesInfoDict():
    Home_Page_Response = getRequest('https://cms.guc.edu.eg/apps/student/HomePageStn.aspx').text
    Home_Page_Html = bs.BeautifulSoup(Home_Page_Response, 'html.parser')
    Html_Files = []
    # Getting Courses info Courses table
    tableID = '#ContentPlaceHolderright_ContentPlaceHoldercontent_GridViewcourses'
    CoursesNames = Home_Page_Html.select(tableID + ' td:nth-child(2)')
    CoursesIDs = Home_Page_Html.select(tableID + ' td:nth-child(5)')
    StudentIDs = Home_Page_Html.select(tableID + ' td:nth-child(6)')
    for i in range(len(CoursesNames)):

        CourseDict = {'Name': re.sub('[|()]', '', CoursesNames[i].getText()) , 'ID': CoursesIDs[i].getText(), 'SID': StudentIDs[i].getText()}
        Html_Files.append(CourseDict)
    return Html_Files

def downloadFile(dir, name, path, ext):
    recieve = getRequest(path)
    with open(dir + name + ext,'wb') as f:
        f.write(recieve.content)

def downloadCourseContent(dirName, id, sid):
    Course_Page_Response = getRequest('https://cms.guc.edu.eg/apps/student/CourseViewStn.aspx?id={id}&sid={sid}'.format(id = id, sid = sid)).text
    Course_Page_Html = bs.BeautifulSoup(Course_Page_Response, 'html.parser')
    downloadableContent = Course_Page_Html.select('.page-title-wrapper #download')
    downloadableContentLabel = Course_Page_Html.select('.page-title-wrapper [class=card-body] div strong')

    for i in range(len(downloadableContent)):
        name = downloadableContentLabel[i].getText()[4:].lstrip()
        path = downloadableContent[i].get('href')
        filename, ext = os.path.splitext(downloadableContent[i].get('href'))
        info = downloadableContentLabel[i].next_sibling
        if (ext != '.mp4' and ext != '.png'):
            if ('lecture' in info.lower()):
                downloadFile(dirName + '/Lectures/', name, 'https://cms.guc.edu.eg/' + path,  ext)
            elif ('practice assignment' in name.lower()):
                downloadFile(dirName + '/Practice Assignments/', name, 'https://cms.guc.edu.eg/' + path,  ext)
            elif ('exam' in info.lower()):
                downloadFile(dirName + '/Exams/', name, 'https://cms.guc.edu.eg/' + path,  ext)
            elif ('quiz' in info.lower() or 'quiz' in name.lower()):
                downloadFile(dirName + '/Quizzes/', name, 'https://cms.guc.edu.eg/' + path,  ext)
            else:
                downloadFile(dirName + '/Others/', name, 'https://cms.guc.edu.eg/' + path,  ext)

def downloadAllCourses():
    CoursesInfo = getCoursesInfoDict()
    for course in CoursesInfo:
        print(course['Name'], course['ID'], course['SID'])
        downloadCourseContent(course['Name'], course['ID'], course['SID'])

downloadAllCourses()
