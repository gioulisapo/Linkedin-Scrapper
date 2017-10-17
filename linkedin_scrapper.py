#!/usr/bin/env python3
from selenium import webdriver
import argparse
# import readline
import getpass
import os as os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time as time
import codecs
import sys
from lxml import html
import requests
import xml
from collections import namedtuple
from bs4 import BeautifulSoup

class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ORANGE ='\033[33m'
    GREY = '\033[97m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def isIDpresent(driver, id):
    try:
        driver.find_element_by_id(id)
        return True
    except:
        return False

def main(argv):
    usage = ("\n   %(prog)s -c <COMPANY NAME> -m <COMPANY MAIL EXTENTION> [--headless]")
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument("-c", "--company", type=str,
                    dest="company", required=True  ,
                    help="Name of company under investigation e.g. Google, Cisco..")
    parser.add_argument("--headless", action="store_true",
                    dest="headless", required=False  ,
                    help="Run in headless mode. PhantomJS presents significant bugs out of yet. Not recommended")
    parser.add_argument("-m", "--companymail", type=str,
                    dest="companymail", required=True  ,
                    help="Mail extention of company under investigation e.g. cisco.com, google.com")

    args = parser.parse_args()
    headless = args.headless
    company = args.company #we need it due to a bug that I couldn't be bothered to fix'
    companymail = args.companymail # need to do some online search to find the company's mail
    
    username = input('['+bcolors.BLUE+'+'+bcolors.ENDC+'] Please provide a valid Linkedin e-mail: ')
    password = getpass.getpass('['+bcolors.BLUE+'+'+bcolors.ENDC+'] Linkedin Password: ')
    url = input('['+bcolors.BLUE+'+'+bcolors.ENDC+'] Please provide the URL of the page displaying the employees that work in the company: ')
    # fix company_mail_format
    if ( "@" not in companymail):
        companymail = "@"+companymail
    mailmode =0
    try:
        mailmode=int(input('['+bcolors.BLUE+'+'+bcolors.ENDC+'] Chose one of the following common company e-mail formats for Mr. John Doe:\n'
        +'    '+bcolors.PURPLE+bcolors.UNDERLINE+'Name First:'+bcolors.ENDC+'\n'
        +bcolors.BLUE+'       1)'+bcolors.ENDC+' JohnD'+companymail+'   '
        +bcolors.BLUE+' 2)'+bcolors.ENDC+' JDoe'+companymail+'   '
        +bcolors.BLUE+' 3)'+bcolors.ENDC+' JohnDoe'+companymail+'\n'
        +bcolors.BLUE+'       4)'+bcolors.ENDC+' john.d'+companymail+'   '
        +bcolors.BLUE+'5)'+bcolors.ENDC+' j.doe'+companymail+'   '
        +bcolors.BLUE+'6)'+bcolors.ENDC+' john.doe'+companymail+'\n'
        +bcolors.BLUE+'       7)'+bcolors.ENDC+' john_d'+companymail+'   '
        +bcolors.BLUE+'8)'+bcolors.ENDC+' j_doe'+companymail+'   '
        +bcolors.BLUE+'9)'+bcolors.ENDC+' john_doe'+companymail+'\n'
        +bcolors.BLUE+'      10)'+bcolors.ENDC+' john-d'+companymail+'  '
        +bcolors.BLUE+'11)'+bcolors.ENDC+' j-doe'+companymail+'  '
        +bcolors.BLUE+'12)'+bcolors.ENDC+' john-doe'+companymail+'\n'
        +'    '+bcolors.PURPLE+bcolors.UNDERLINE+'Surname First:'+bcolors.ENDC+'\n'
        +bcolors.BLUE+'      13)'+bcolors.ENDC+' DJohn'+companymail+' '
        +bcolors.BLUE+' 14)'+bcolors.ENDC+' DoeJ'+companymail+'   '
        +bcolors.BLUE+' 15)'+bcolors.ENDC+' DoeJohn'+companymail+'\n'
        +bcolors.BLUE+'      16)'+bcolors.ENDC+' deo.j'+companymail+'  '
        +bcolors.BLUE+'17)'+bcolors.ENDC+' d.john'+companymail+'  '
        +bcolors.BLUE+'18)'+bcolors.ENDC+' doe.john'+companymail+'\n'
        +bcolors.BLUE+'      19)'+bcolors.ENDC+' doe_j'+companymail+'  '
        +bcolors.BLUE+'20)'+bcolors.ENDC+' d_john'+companymail+'  '
        +bcolors.BLUE+'21)'+bcolors.ENDC+' doe_john'+companymail+'\n'
        +bcolors.BLUE+'      22)'+bcolors.ENDC+' doe-j'+companymail+'  '
        +bcolors.BLUE+'23)'+bcolors.ENDC+' d-john'+companymail+'  '
        +bcolors.BLUE+'24)'+bcolors.ENDC+' doe-john'+companymail+'\n    (1-24): '))
    except ValueError:
        print ("["+bcolors.RED+"!"+bcolors.ENDC+"] Please provide a number between 1-24")
        sys.exit(0)
    if (mailmode < 1 or mailmode > 24):
        print ("["+bcolors.RED+"!"+bcolors.ENDC+"] Please provide a number between 1-24")
        sys.exit(0)

# TODO
    # Should Middle name be considered when present?
    middleflag=False
    # middlechoice=input('['+bcolors.BLUE+'+'+bcolors.ENDC+'] Should Middle name be used when present? e.g.'+bcolors.GREY+' j_m_doe, JMDoe, doe-m-john:\n    (y/n): ')
    # if (middlechoice == "y" or middlechoice == "yes" or middlechoice == "Y" or middlechoice == "YES"  or middlechoice == "Yes"):
    #     middleflag=True
# END TODO

    if (headless):
        try:
            driver = webdriver.PhantomJS()
        except:
            print ("["+bcolors.RED+"+"+bcolors.ENDC+"] Please install PhantomJS")
            print ("\t"+bcolors.BLUE+"arch-based  : "+bcolors.ENDC+"yaourt -S phantomjs")
            print ("\t"+bcolors.BLUE+"debian-based: "+bcolors.ENDC+"sudo apt-get install build-essential chrpath libssl-dev libxft-dev libfreetype6-dev libfreetype6 libfontconfig1-dev libfontconfig1 -y;\n\t\t      sudo wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2;\n\t\t      sudo tar xvjf phantomjs-2.1.1-linux-x86_64.tar.bz2 -C /usr/local/share/;\n\t\t      sudo ln -s /usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/;\n\t\t      phantomjs --version")
            print ("\t"+bcolors.BLUE+"Windows     : "+bcolors.ENDC+"Donwload and extract PhantomJS in linkedin_scraper folder.")
            sys.exit(0) 
    else:
        try:
            driver = webdriver.Firefox()
        except:
            print ("["+bcolors.RED+"+"+bcolors.ENDC+"] Please install https://github.com/mozilla/geckodriver/releases/download/")
            print ("\t"+bcolors.BLUE+"arch-based  : "+bcolors.ENDC+"yaourt -S geckodriver")
            print ("\t"+bcolors.BLUE+"debian-based: "+bcolors.ENDC+"Downolad latest release from here: https://github.com/mozilla/geckodriver/releases\n\t\t      Extract, make executable and place geckodriver in your PATH.")
            print ("\t"+bcolors.BLUE+"Windows     : "+bcolors.ENDC+"Donwload and extract PhantomJS in linkedin_scraper folder.")
            sys.exit(0)
    print('['+bcolors.BLUE+'+'+bcolors.ENDC+'] Intialising...')
    driver.get(r"https://www.linkedin.com/")
    try:
        element = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.ID, "login-password"))
        )
    except:
        pass
    print('['+bcolors.BLUE+'+'+bcolors.ENDC+'] Logging in...')
    inputElement = driver.find_element_by_id("login-email")
    inputElement.send_keys(username)
    inputElement = driver.find_element_by_id("login-password")
    inputElement.send_keys(password)
    inputElement = driver.find_element_by_id("login-submit")
    inputElement.submit() 
    time.sleep(3)
    if (isIDpresent(driver, "session_password-login-error")):
        print('['+bcolors.RED+'+'+bcolors.ENDC+'] Wrong Password. Please provide valid credentials')
        sys.exit(0)
    try:
        driver.get(url)
    except:
        # print('['+bcolors.RED+'+'+bcolors.ENDC+'] Wrong URL provided: "'+bcolors.ORANGE+''+url+bcolors.ENDC+'"\n    Please Provide correct URL.')
        # There is a bug with PhantmJS driver can't get URL. Creating new driver fixes it.
        driver = webdriver.PhantomJS()
        driver.get(url)
        # sys.exit(0)
    time.sleep(4)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    completeName = os.path.join("./", "bot_results.html")
    file_object = codecs.open(completeName, "a", "utf-8")
    html = driver.page_source
    file_object.write(html)
    print('['+bcolors.BLUE+'+'+bcolors.ENDC+'] Scrapping Intialised.')
    #progress_bar
    toolbar_width = 100 #presumably....

    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

    #start getting info
    while True:
        try:
            next_button = driver.find_element_by_class_name('next')
            next_button.click()
        except:     #sometimes the page is not fully loaded so the next button can't be clicked'
            time.sleep(1)
            try:
                next_button = driver.find_element_by_class_name('next')
                next_button.click()
            except:
                print('\n['+bcolors.BLUE+'+'+bcolors.ENDC+'] Finished Scraping Stage.')
                break
        time.sleep(3) #would't go below 1'
        html = driver.page_source
        file_object.write(html)
        #progress_bar
        sys.stdout.write("=")
        sys.stdout.flush()
    file_object.close()
    HtmlparserToXML(company)
    Link_Scraper(company, companymail, mailmode, middleflag)

def HtmlparserToXML(company):
    '''
        Takes all the html stored in the bot_results.html file, deletes it, extracts the usefull info and parses it in an xml file 
    '''
    print('['+bcolors.BLUE+'+'+bcolors.ENDC+'] Parsing to XML')
    target = open(company+'_results.xml', 'w')
    with open('./bot_results.html', "r") as f:
        page = f.read()
    f.close()
    tree = html.fromstring(page)


    #This will create a list of buyers:
    name = tree.xpath('//span[@class="name actor-name"]/text()')
    firstName = []
    lastName = []
    for x in name :
        firstName.append(x.split( )[0])
    for x in name :
        lastName.append(x.split( )[1])
    fmt_headline = list(tree.xpath('//p[@class="subline-level-1 Sans-15px-black-85% search-result__truncate"]/text()'))
    current = tree.xpath('//p[@class="search-result__snippets mt2 Sans-13px-black-55% ember-view"]/text()')

    target.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    target.write("<persons>\n")
    for i in range (0,len(firstName)):
        if 'LinkedIn' in firstName[i]:
            continue
        target.write("\t<person>\n")
        target.write("\t\t<firstName>"+firstName[i].replace("&","and")+"</firstName>\n")
        target.write("\t\t<lastName>"+lastName[i].replace("&","and")+"</lastName>\n")
        target.write("\t\t<fmt_headline>"+fmt_headline[i].replace("&","and")+"</fmt_headline>\n")
        target.write("\t\t<current>"+current[i].replace("&","and").replace("at","at "+company)+"</current>\n")
        target.write("\t</person>\n")
    target.write("</persons>\n")
    target.close()


def Mail_Maker(name, lastname, companymail, mailmode, middleflag):
    '''
        Depending on the option provided by the user it crafts the email of <name> <LastName>
    '''
    name = name.lower()
    lastname = lastname.lower()
    def f(mailmode):
        return {
            1: name+lastname[0]+companymail,
            2: name[0]+lastname+companymail,
            3: name+lastname+companymail,
            4: name+"."+lastname[0]+companymail,
            5: name[0]+"."+lastname+companymail,
            6: name+"."+lastname+companymail,
            7: name+"_"+lastname[0]+companymail,
            8: name[0]+"_"+lastname+companymail,
            9: name+"_"+lastname+companymail,
            10: name+"-"+lastname[0]+companymail,
            11: name[0]+"-"+lastname+companymail,
            12: name+"-"+lastname+companymail,
            13: lastname+name[0]+companymail,
            14: lastname[0]+name+companymail,
            15: lastname+name+companymail,
            16: lastname+"."+name[0]+companymail,
            17: lastname[0]+"."+name+companymail,
            18: lastname+"."+name+companymail,
            19: lastname+"_"+name[0]+companymail,
            20: lastname[0]+"_"+name+companymail,
            21: lastname+"_"+name+companymail,
            22: lastname+"-"+name[0]+companymail,
            23: lastname[0]+"-"+name+companymail,
            24: lastname+"-"+name+companymail,
        }[mailmode]
    return f(mailmode)

def Link_Scraper(company, companymail, mailmode, middleflag):
    '''
        takes the extracted info by the HtmlparserToXML() method and creates a list of usernames.
        It also creates a list of Names and coresponding job titles. 
    '''
    print('['+bcolors.BLUE+'+'+bcolors.ENDC+'] Creating Emails')
    Employee = namedtuple('Employee', 'firstName lastName headline current')
    employees = []
    results = open(company+"_results.xml").read()
    soup = BeautifulSoup(results   , "xml")
    target_1 = open('emails_'+company+'.txt', 'w')
    target_2 = open('job_roles_'+company+'.txt', 'w')

    firstNames = []
    lastName = []
    fmt_headline = []
    current = []
    for name in soup.findAll("firstName"):
        firstNames.append(name.string)
    for name in soup.findAll("lastName"):
        lastName.append(name.string)
    for name in soup.findAll("fmt_headline"):
        fmt_headline.append(name.string)
    for name in soup.findAll("current"):
        current.append(name.string)

    for person in range(0,len(firstNames)):
        if 'LinkedIn' in firstNames[person]: #Users called LinkedIn Member are useless for our purposes
            continue
        else:
            emp = Employee(firstNames[person], lastName[person], fmt_headline[person], current[person])
            employees.append(emp)

    for employee in employees:
        target_1.write((Mail_Maker(employee.firstName, employee.lastName, companymail,mailmode, middleflag)))
        target_1.write('\n')
        target_2.write(employee.firstName+" "+employee.lastName)
        target_2.write(("\t\t" + employee.headline+'\n'))
    os.remove('./bot_results.html')
    os.remove('./'+company+'_results.xml')

if __name__ == "__main__":
   main(sys.argv[1:])