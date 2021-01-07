import bs4,sys,threading
import pyinputplus as pyip
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#sets up the name of the show
if(len(sys.argv)>2):
   name = ' '.join(sys.argv[1:])
elif(len(sys.argv)==2):
   name = sys.argv[1]
else:
    name = input("What show/movie?: ")
print('Loading...')
url = 'https://www.imdb.com/'
driver = webdriver.Firefox(executable_path='C:\\Users\\aksha\\Downloads\\geckodriver-v0.28.0-win64\\geckodriver.exe')
driver.get(url)
driver.minimize_window()

#searches for the name on imdb
userElem = driver.find_element_by_id('suggestion-search')
userElem.send_keys(name)
userElem.send_keys(Keys.ENTER)
try:
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "findMoreMatches"))).click()
except TimeoutException:
    pass
options = driver.find_elements_by_class_name('result_text')

#gives the results of the search and lets you choose which one you want
if(len(options)<3):
    for x in range(len(options)):
        print(str(x+1) + '. ' + options[x].text)
        print('\n')
    choice = pyip.inputInt("Which one do you want (must use a num): ",min=1,max=len(options))
else:
    for x in range(3):
        print(str(x + 1) + '. ' + options[x].text)
        print('\n')
    choice = pyip.inputInt("Which one do you want (print 0 if none of these): ", min=0, max=3) - 1
if(choice == -1):
    for x in range(len(options)):
        print(str(x+1) + '. ' + options[x].text)
        print('\n')
    choice = pyip.inputInt("Which one do you want (must use a num): ",min=1,max=len(options))
print('Loading...')

#bring you to the url of the user reviews page
url = driver.find_elements_by_class_name('result_text')[choice].find_element_by_css_selector('a').get_attribute('href')
url = 'https://www.imdb.com/title/'+url[27:url.find('/?')]+'/reviews?ref_=tt_ql_3'

driver.get(url)

#load button spam to load all of the reviews
numClicked = 0
while(True):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ipl-load-more__button"))).click()
    except TimeoutException:
        break
    numClicked+=1
    if(numClicked == 50):
        break



#adds reviews to a list
html = driver.page_source
soup = bs4.BeautifulSoup(html,'html.parser')
reviews = soup.find_all(class_='text show-more__control')
reviews += soup.find_all(class_='text show-more__control clickable')
print('{} reviews found'.format(len(reviews)))

#VADER SENTIMENT ANALYSIS on each review
analyzer = SentimentIntensityAnalyzer()
avgVader = 0
numPos = 0
numNeg = 0
avgPos = 0
avgNeg = 0
numNeutral = 0
def analyze(start,end):
    global reviews
    global avgVader, numPos, avgPos, avgNeg, numNeg, avgVader,numNeutral
    i = start//200

    if(end>len(reviews)):
        end = len(reviews)
    for x in range(start,end):

        try:
            reviews[x] = str(reviews[x]).replace('<div class="text show-more__control">','').replace('<div class="text show-more__control clickable">','').replace('</div>','').replace('<br/>','')
            score = analyzer.polarity_scores(reviews[x])['compound']
            avgVader+=score
            if(score>0.05):
                numPos+=1
                avgPos+=score
            elif(score<-0.05):
                numNeg+=1
                avgNeg+=score
            elif(score<=0.05 and score>=-0.05):
                numNeutral+=1
            else:
                print(score)
        except TypeError as e:
            print(e)

downloadThreads =[]
for x in range(0,len(reviews),200):
    start = x
    end = x + 199
    downloadThread = threading.Thread(target=analyze, args=(start, end))
    downloadThreads.append(downloadThread)
    downloadThread.start()

for downloadThread in downloadThreads:
    downloadThread.join()



if(numNeg == 0 and avgNeg == 0):
    avgNeg = 0
else:
    avgNeg = avgNeg/numNeg
if(numPos == 0 and avgPos == 0):
    avgPos == 1
else:
    avgPos = avgPos/numPos
#Cleans up the data
if(len(reviews) != 0):
    avgVader = avgVader/len(reviews)

print('There were {} reviews retrieved'.format(len(reviews)))
print('There are {} positive reviews and {} negative reviews'.format(numPos,numNeg))
print('The average positive score was : {} \nThe average negative score was : {}'.format(avgPos,avgNeg))
print('The average score was : ' + str(avgVader))
VaderScore = round(avgVader*5+5,1)
print('VADER says : {} death stars out of 10'.format(VaderScore))
driver.quit()

if(numNeutral+numNeg+numPos!=len(reviews)):
    print("Error Somewhere, numReviews != numTotal")
    print(str(numNeutral))


