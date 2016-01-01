import sys,re,glob,numpy
from bs4 import BeautifulSoup

def unique(list_of_dicts):
    return list(numpy.unique(numpy.array(list_of_dicts)))

def short(string):
    temp = re.sub(r'AND|OF|THE|&', "", string).split()
    str = ''
    for x in temp:
        str += x[0]
    return str

def extractInfo(file):
    soup = BeautifulSoup(file, 'html.parser')

    infoTable = soup.findAll("b")

    roll = soup.find("td", class_="formHeading4").string
    name = infoTable[1].string
    college = infoTable[2].string
    branch = infoTable[3].string

	# Getting Short College Name
    temp = re.sub(r'AND|OF|THE|&', "", college).split(",")
    clgname = short(temp[0])
    clgcity = temp[1].split()[0]
    shortCollege = clgname+" "+clgcity

	# Finding Short Branch Name
    shortBranch = short(branch)

    return ((roll,shortBranch,branch,name),soup)

def extractResults(soup):
    result = []
    # row = soup.findAll("table", class_="formTextWithBorder")[1].findAll("td")
    # There are 6 columns: Sl.No. | Subject Code | Subject | Credits | Grade | Date
    table = soup.findAll("table", class_="formTextWithBorder")[1]
    subjects = table.findAll("td", attrs = {"width":"49%"})[1:]
    for subject in subjects:
        # In the form: subject, subjectCode, subjectCredit, subjectGrade
        result += ((subject.string, subject.findPrevious().string, subject.findNext().string, subject.findNext().findNext().string),)
    sgpa = table.find("td", attrs = {"colspan":"2"}).contents[1]
    return result,sgpa.strip()

def filesOf(batch,sem):
    if batch == 2018:
        semcodes = [485, 526]

    elif batch == 2017:
        semcodes = [345,398,473,525]

    elif batch == 2016:
        semcodes = [253, 299, 340, 393, 468, 524]

    elif batch == 2015:
        semcodes = [195, 204, 248, 294, 335, 388, 464, 523]

    elif batch == 2014:
        semcodes = [108, 149, 185, 203, 243, 290, 331, 384]

    semcode = semcodes[sem-1]

    files = glob.glob("data/%d/%d/*.html" % (batch, semcode))
    #files = ["data/2017/345/1301106071.html"]
    return files

# Accumulate Branches
def getBranches(batch = 2017):
    sem = 1
    branches = []

    for x in filesOf(batch,sem):
        file = open(x)
        info = extractInfo(file)

        branches.append({'shortName':info[0][1],'fullName':info[0][2]})

    branches = unique(branches)
    return branches

# print getBranches()

# Accumulate Semesters
def getSemesters():
    # {'batch': 2017, 'num': 1, 'code': 345}
    data = [
    {2018: [485, 526]},
    {2017: [345,398,473,525]},
    {2016: [253, 299, 340, 393, 468, 524]},
    {2015: [195, 204, 248, 294, 335, 388, 464, 523]},
    {2014: [108, 149, 185, 203, 243, 290, 331, 384]}]
    
    semesters = []

    for x in data:
        batch = x.keys()[0]
        for y in x.values():
            for z in range(1, len(y)+1):
                semesters.append({'batch' : batch, 'num' : z, 'code' : y[z-1]})

    return semesters

# print getSemesters()

# Accumulate Subjects
def getSubjects():
    # {'code':'BSIT4302', 'name':'Data Structures', 'credits':4}
    data = {2018: 2, 2017: 4, 2016: 6, 2015: 8, 2014: 8}
    subjects = []

    for x in data:
        batch = x
        lastSem = data[x]
        for sem in range(1,lastSem+1):
            print "%d [%d]" % (batch,sem)
            for x in filesOf(batch,sem):
                file = open(x)
                soup = BeautifulSoup(file, 'html.parser')
                y = extractResults(soup)[0]
                file.close()
                for z in y: subjects.append({'code' : z[1], 'name' : z[0], 'credits' : int(z[2])})
        subjects = unique(subjects)

    return subjects

print getSubjects()

# Accumulate Students
# Accumulate Exams
# Accumulate Scores


# print "%s %-3s %-30s" % info[0]
# subjects,sgpa = extractResults(info[1])
# for subject in subjects: print "%-34s %s %s %s" % subject
# print "SGPA: [%s]" % sgpa