import sys,re,requests,os
from bs4 import BeautifulSoup
from time import sleep
from random import randint

def extractInfo(file):
    soup = BeautifulSoup(file, 'html.parser')

    infoTable = soup.findAll("b")

    #roll = infoTable[0].string
    name = infoTable[1].string
    college = infoTable[2].string
    branch = infoTable[3].string

	# Getting Short College Name
    temp = re.sub(r'AND|OF|THE|&', "", college).split(",")
    clgname = ''
    for x in temp[0].split():
	    clgname += x[0]
    clgcity = temp[1].split()[0]
    shortCollege = clgname+" "+clgcity

	# Finding Short Department Name
    temp = re.sub(r'AND|OF|&', "", branch).split()
    shortBranch = ""
    for x in temp:
        shortBranch += x[0]

    return (roll,shortCollege,shortBranch,name)

def getFile(batch, semcode, roll):
    file = "data/%d/%d/%d.html" % (batch, semcode, roll)
    if os.path.exists(file):
        return open("data/%d/%d/%d.html" % (batch, semcode, roll))
    else:
        return downloadFile(batch, semcode,roll)

def downloadFile(batch, semcode, roll):
    directory = "data/%d/%d/" % (batch,semcode)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    if randint(0,9)%2 == 0:
        sleep(0.5)
        print "Sleeping."
    
    res = requests.get("http://results.bput.ac.in/%d_RES/%d.html" % (semcode,roll))

    if res.status_code == 200:
        file = ""
		
        print "%d downloading." % roll,
        resFile = open("data/%d/%d/%d.html" % (batch,semcode,roll), "wb")

        for chunk in res.iter_content(1000):
            resFile.write(chunk)
            file += chunk
        resFile.close()
        print " Done."
        return file
    else:
        return res.status_code

batch = int(sys.argv[1])
if batch == 2018:
    #2018 batch
    semcodes = [485, 526]

    start = 1401106000
    end = 14011067000
    le_start = 1521106000
    le_end = 1521106200

elif batch == 2017:
    #2017 batch
    semcodes = [345,398,473,525]

    start = 1301106000
    end = 1301106610
    le_start = 1421106000
    le_end = 1421106170

elif batch == 2016:
    # 2016 batch
    semcodes = [253, 299, 340, 393, 468, 524]

    start = 1201106000
    end = 1201106600
    le_start = 1321106000
    le_end = 1321106200

elif batch == 2015:
    #2015 batch
    semcodes = [195, 204, 248, 294, 335, 388, 464, 523]

    start = 1101106000
    end = 1101106400
    le_start = 1221106000
    le_end = 1221106100

elif batch == 2014:
    #2014 batch
    semcodes = [108, 149, 185, 203, 243, 290, 331, 384]

    start = 1001106000
    end = 1001106500
    le_start = 1121106000
    le_end = 1121106200

semcode = semcodes[int(sys.argv[2])-1]

i = 0 # Count of students

for roll in range(start, end+1)+range(le_start,le_end+1):
    #print " [%d]" % roll,
    file = getFile(batch,semcode,roll)
    if file != 404:
        info = extractInfo(file)
        i += 1
        if info[1] != "CET BHUBANESWAR":
            os.remove("data/%d/%d/%d.html" % (batch,semcode, roll))
            print "deleting %d ! " % roll,
	    
        print "%d %s %-3s %s" % info

print "Done with semcode: %d. Found %d students" % (semcode,i)
