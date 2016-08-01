from models import *
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

b = webdriver.Firefox() #browser

students = Student.select(Student.regno).where((Student.batch == 2017) &
    (Student.branch == 'EE'))
# students = [{'regno':1301106071}, {'regno': 1301106267}, {'regno':1301106021}]

b.get('http://bputexam.in/StudentSection/ResultPublished/StudentResult.aspx')
b.find_element_by_id('dpStudentdob_dateInput').send_keys('1/1/2015')

for student in students:
    reg_ip = b.find_element_by_id('txtRegNo')
    reg_ip.clear()
    reg_ip.send_keys(student.regno)
    b.find_element_by_id('btnView').click()
    try:
        result_links = b.find_elements_by_link_text('View Result')
        #for link in results_link:
        link = result_links[-1]
        link.click()

        exam = b.find_element_by_id('lblResultName')
        exam = exam.text.split(',')[-1].strip()

        name = b.find_element_by_id('lblName')
        name = name.text.title()

        result_table = b.find_element_by_id('gvViewResult')
        sgpa_span = result_table.find_element_by_css_selector("tbody > tr:last-child > td:last-child > span")
        sgpa = sgpa_span.text.split(':')[-1].strip()

        print exam, '-', name , ' : ', sgpa

        filename = 'dump/%s/%s.html' % (exam, student.regno+' - '+name)

        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(filename, 'wb') as f:
            f.write(b.page_source.encode('utf-8'))
            f.close()
            # print 'Saved ', student.regno

    except Exception as err:
        print "Error for: "+student.regno
        continue
