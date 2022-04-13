import traceback
from django.shortcuts import render
from django.http import HttpResponse
from .scrapers import *
from .models import search as search2
from .models import history as history2
from datetime import datetime
import datetime as dt
import json
import csv
from threading import Thread
import time
import pytz

def home(request):
        return render(request,'home.html')


def search_history(request):
        return render(request,'search_history.html')


def init_search(keywords, websites):
#    uc.install(executable_path = '/home/akash/scraping_app/chromedriver')
    # options = uc.ChromeOptions()
#*    options = webdriver.ChromeOptions()
#*    options.add_argument("start-maximized")
#    options.add_argument('--disable-blink-features=AutomationControlled')
#    options.headless=True
#    options.add_experimental_option('useAutomationExtension', False)
#*    options.add_argument('--disable-dev-shm-usage')
#*    options.add_argument('--disable-gpu')
#*    options.add_argument('--no-sandbox')
#*    options.add_argument('--headless')
    # chrome_path = '/home/akash/scraping_app_env/lib/python3.8/site-packages/chromedriver_binary/chromedriver'
#*    options.headless = True
    # remove the executable_path argument while running on windows
#*    ex_path =  '/home/scraper/scraping_app/chromedriver'
#*    driver = uc.Chrome(executable_path = ex_path, options=options)
#*    time.sleep(1)

    scraper = Scraper(keywords, websites)
    scraper.scrape()
    return scraper.result


def write(result, websites=None, keywords=None):
    data = []
    datetime1= datetime.now(pytz.timezone('Europe/Athens'))
    for i,r in result.iterrows():
        data.append(dict(r))
        keywords, website, title, price, availibility = list(r)

        ins=search2(date=datetime1,keywords=keywords,websites=website,
            title=title,price=price,availibility=availibility)
        ins.save()

    ins1=history2(date=datetime1,keywords=keywords,websites=', '.join(websites))
    ins1.save()
    print("Data saved to database")
    return data


class Scheduler(Thread):

    def __init__(self,time, keywords, websites):
        Thread.__init__(self)
        self.time = time
        self.keywords = keywords
        self.websites = websites
        self.stop = False
        print('__init__ Scheduler')

    def run(self):
        print("thread run")

        while not self.stop:
            #print('in while', start)
            timenow = datetime.now(pytz.timezone('Europe/Athens'))
            if timenow.hour == int(self.time[:2]) and timenow.minute == int(self.time[2:]):
                print('Scheduled scrape- ', self.keywords, self.websites, self.time)
                write(init_search(self.keywords, self.websites), self.websites, self.keywords)
            
            time.sleep(32)



sch = Thread()

def search(request):
    print('\n\n')
    global sch
    if request.method=="POST":
        try:
            #raise Exception
            keywords = request.POST.get('keywords')
            print("Keywords:", keywords)

            sch_inp = request.POST.get('scheduler')
            print('\n', dict(request.POST))
            if sch_inp.isalpha() and sch_inp.lower()=='stop':
                if sch:
                    sch.stop = True
                return render(request, 'search.html', {'sch_status': 'Schedule removed' if sch.is_alive() else ''})

            if (not sch_inp.isdigit() or len(sch_inp)!=4) and sch_inp:
                return render(request, 'search.html', {'error': 'Invalid input- enter a four digit number (hhmm) or "stop"'})
           
            set_time = sch_inp
            websites = list(request.POST)[2:-1]
            print('Websites:', websites)
            print('Frequency', set_time, '\n')

            if not set_time:
                #time.sleep(3)
                result = init_search(keywords, websites)
                data = write(result, websites, keywords)
                woman = {"sch_status": f"Schedule set at {str(sch.time)[:2]}:{str(sch.time)[2:]}hrs (Enter 'stop' to stop last schedule)" if sch.is_alive() else '', 'status': "Search successful. Database updated."}
                return render(request, 'search.html', woman)
            else:
                if sch.is_alive():
                    sch.stop = True

                sch = Scheduler(str(set_time), keywords, websites)
                sch.start()
                data = {"sch_status": f"Schedule set at {str(sch.time)[:2]}:{str(sch.time)[2:]}hrs (Enter 'stop' to stop last schedule)" if sch.is_alive() else ''}
                return render(request, 'search.html', data )
        except BaseException as e:
            with open('/home/scraper/scraping_app/errors.txt', 'a') as f:
                f.write('\n'+ str(datetime.now(pytz.timezone('Europe/Athens'))) + traceback.format_exc() + '*'*50 + '\n')

            return render(request, 'search.html',{'error': 'An Error occured while processing the request.'} )
    else:
        return render(request, 'search.html', {"sch_status": f"Schedule set at {str(sch.time)[:2]}:{str(sch.time)[2:]}hrs (Enter 'stop' to stop last schedule)" if sch.is_alive() else ''})



list1=[]
def show_history(request, history_id):

    history= history2.objects.get(pk=history_id)
    date=history.date
    #print(type(date), date)
    global list1
    list1 = search2.objects.all().filter(date=date)
    #print(type(list1),list1)

    return render(request,'show_history.html',{'list1':list1})


def history(request):
        history_list = history2.objects.all().order_by('-date')[:50]
        return render(request,'history.html',
                {'history_list':history_list})


def history_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=show_history.csv'
    #list1=show_history.list1
    global list1
    writer=csv.writer(response)
    writer.writerow(['Date-Time','keywords','websites','title','price','availability'])

    for i in list1:
        writer.writerow([i.date, i.keywords, i.websites, i.title, i.price, i.availibility])

    return(response)
