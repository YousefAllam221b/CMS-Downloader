import requests
from requests_ntlm import HttpNtlmAuth
import bs4 as bs
import re
import os

# Runs the script in the choosen directory.
mainDir = r'C:\Users\Youse\Documents\Semester 6'
os.chdir(mainDir)

# Makes a get request
def getRequest(path):
    recieve = requests.get(path, auth = HttpNtlmAuth('yousef.alam', 'JohnWatson123!'))
    return recieve

# Gets Courses info (Name, ID and SID) from cms main page.
def getCoursesInfo():
    # Gets the HTML file of the CMS Main Page
    Home_Page_Response = getRequest('https://cms.guc.edu.eg/apps/student/HomePageStn.aspx').text
    Home_Page_Html = bs.BeautifulSoup(Home_Page_Response, 'html.parser')
    CoursesInfo = []
    # Getting Courses info Courses table
    tableID = '#ContentPlaceHolderright_ContentPlaceHoldercontent_GridViewcourses'

    # Gets Names, IDs and SIDs of each Course
    CoursesNames = Home_Page_Html.select(tableID + ' td:nth-child(2)')
    CoursesIDs = Home_Page_Html.select(tableID + ' td:nth-child(5)')
    StudentIDs = Home_Page_Html.select(tableID + ' td:nth-child(6)')

    # Loops on each row of the table (Course) and append it's Info in CourseInfo array
    for i in range(len(CoursesNames)):
        CourseDict = {'Name': re.sub('[|()]', '', CoursesNames[i].getText()) , 'ID': CoursesIDs[i].getText(), 'SID': StudentIDs[i].getText()}
        CoursesInfo.append(CourseDict)
    return CoursesInfo

# Downloads a file
def downloadFile(dir, name, path, ext):
    # Gets the file from the server
    recieve = getRequest(path)
    # Save the file in the Given directory under the given name
    with open(dir + name + ext,'wb') as f:
        f.write(recieve.content)

def downloadCourseContent(dirName, id, sid):
    # Gets the HTML file of a Course given it's ID and SID.
    Course_Page_Response = getRequest('https://cms.guc.edu.eg/apps/student/CourseViewStn.aspx?id={id}&sid={sid}'.format(id = id, sid = sid)).text
    Course_Page_Html = bs.BeautifulSoup(Course_Page_Response, 'html.parser')

    # Selects Labels and Download buttons for all available downloadable Content
    downloadableContentLabel = Course_Page_Html.select('.page-title-wrapper [class=card-body] div strong')
    downloadableContent = Course_Page_Html.select('.page-title-wrapper #download')

    for i in range(len(downloadableContent)):
        # Chooses the file name from it's Label, it's type (which folder),it's download link and it's extension.
        name = downloadableContentLabel[i].getText()[4:].lstrip()
        path = downloadableContent[i].get('href')
        filename, ext = os.path.splitext(downloadableContent[i].get('href'))
        info = downloadableContentLabel[i].next_sibling

        # Checks the extension and the type of file to save it to the rigth folder.
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

# Download all files
def downloadAllCourses():
    CoursesInfo = getCoursesInfo()
    for course in CoursesInfo:
        print(course['Name'], course['ID'], course['SID'])
        downloadCourseContent(course['Name'], course['ID'], course['SID'])

downloadAllCourses()
