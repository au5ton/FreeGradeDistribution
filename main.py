from createMasterDB import createMasterDBs
from downloadPDFs import downloadPDFs
from googleOCR import googleOCR
from manipulatePDFs import manipulatePdfs
from outputData import outputData
from openpyxl import Workbook
import os
from os import path

from glob import glob

_author_ = "Marcus Salinas"


def find_ext(dr, ext):
    return glob(path.join(dr, "*.{}".format(ext)))


def getSemesterChar(semester):
    if semester == "Spring":
        return "A"
    elif semester == "Summer":
        return "B"
    elif semester == "Fall":
        return "C"
    else:
        return "N/A"

def semesterCharToURLChar(semesterChar):
    if semesterChar == "A":
        return "1"
    elif semesterChar == "B":
        return "2"
    elif semesterChar == "C":
        return "3"
    else:
        return "0"

# url = "http://web-as.tamu.edu/gradereport/PDFReports/"
url = "http://web-as.tamu.edu/gradereport/"
listOfColleges = [
    "AG",  # AGRICULTURE AND LIFE SCIENCES
    "AR",  # ARCHITECTURE
    "BA",  # BUSINESS
    "ED",  # EDUCATION Spring 2016
    #"EL",  # ENGLISH LANGUAGE INSTITUTE No access 3/16/2017
    "EN",  # ENGINEERING
    "GB",  # GEORGE BUSH SCHOOL OF GOVERNMENT
    "GE",  # GEOSCIENCES
    "LA",  # LIBERAL ARTS Spring 2014
    "MD", # MEDICINE No longer have access
    "MS",  # MILITARY SCIENCE
    "SC",  # SCIENCE
    "VM"  # VETERINARY MEDICINE
]

listOfSemesters = [
    #"Spring",  # A
    # "Summer",  # B
     "Fall"  # C
]

year = 2016
MainDirectory = os.getcwd()
for semester in listOfSemesters:
    print ("On Semester: " + semester)
    os.chdir(MainDirectory)
    semesterChar = getSemesterChar(semester)
    folderName = semester + str(year)
    pdfFileDirectory = os.getcwd() + "/GradeDistributionsDB/" + folderName
    yearAndURLChar = str(year) + semesterCharToURLChar(semesterChar)
    # # Part 1a
    # # get the data from the website
    for x in range(0, len(listOfColleges)):
        print("On College: " + str(listOfColleges[x]))
        downloadPDFs(url, str(year), semesterChar, listOfColleges[x])

    os.chdir(pdfFileDirectory)
    # # Part 1b
    # take the pdfs and make them to text files
    # pdfList = glob('*.pdf')
    # googleOCR(folderName, pdfList)

    # Part 2a
    # take all the data we have right now and give us what we need
    txtList = glob('*.txt')
    for textFile in txtList:
        os.chdir(MainDirectory)
        print ("On TextFile " + textFile)
        college = textFile[8:10]
        masterDictionary = manipulatePdfs(textFile, semester, str(year))

        # Part 2b
        # take the data we have and make it useful
        title = semester + str(year) + " " + college + ".xlsx"
        wb = Workbook()

        # save the file to a new path
        newPath = os.getcwd() + "/Output"
        if not os.path.exists(newPath):
            os.makedirs(newPath)
        os.chdir(newPath)

        # call the function to outpt data and save in the new path
        wb = outputData(masterDictionary, title)
        wb.save(title)

# finally we just run the createMaster DB file
os.chdir(MainDirectory)
createMasterDBs(listOfColleges)
