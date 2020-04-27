#!/usr/bin/env python
# coding: utf-8




import requests
import json
import time
from  datetime import datetime  as dt
from bs4 import BeautifulSoup
from copy import deepcopy



import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# import socks
# #socks.setdefaultproxy(TYPE, ADDR, PORT)
# socks.setdefaultproxy(socks.SOCKS5, '172.31.2.3', 8080)
# socks.wrapmodule(smtplib)


# A driver code to end email as an alert
def sendMail(body,toaddr):
    global error
    fromaddr = "from_address@mail.com"    
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = ', '.join(toaddr)
    msg['Subject'] = "Avengers Tickets are Open"
    msg.attach(MIMEText(body, 'plain','utf-8'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    try:
        server.login(fromaddr, "password_of_sending_mailer")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
    except:
        error = error + 'ERROR: Mailing error at '+ str(dt.now()) + '\n'
        print(error)




# url is where to check the status of movies
def getSoup(url = 'https://paytm.com/movies/allahabad'):
    global error,me
    html=''
    soup = ''
    try:
        start = time.time()
        response = requests.get(url)
        print("Access Time: ",time.time()-start)
        # If the site maintenance is happenening, it implies a possible update in website
        if response.status_code != 200:
            print('$hit')
            msg = 'ERROR: PAYTM Access at : {} \n'.format(str(dt.now()))
            # send an alert to make sure
            error += msg
            sendMail(msg,me)
        html = response.text
        
        soup = BeautifulSoup(html, 'lxml')
    except:
        # raise error and alert if something goes wrong
        msg = 'ERROR: PAYTM Site at : {} \n'.format(str(dt.now()))
        error += msg
        sendmail(msg,me)
      
    return soup

# function to check any updation in the movie list
def testMovie(new):
    global prev,error,message,me,toaddr
    flag = False
    titles = ' '.join(new)

    if any( title not in prev for title in new):
        flag= True
        error += 'Yay Found New Movie at {} \n'.format(str()) 
        message += 'Yay Found New Movie at {} \n'.format(str()) 
        print('Yay Found New Movie')
        message += titles
        sendMail(message , toaddr)    
    
    flag1 = False
    if any(s in titles.lower() for s in ['avengers' , 'end' , 'game', 'marvel']) :
        flag1 = True
        print('Got it. at ' + str(dt.now()))

    return flag or flag1

def findMovie(soup):
    global prev,error,message,me,toaddr

    # these are some class ID used by the website for their content
    try :
        movies = soup.findAll('div', {'class': '_1xgL'})
        running = movies[0].findAll('div', {'class': '_3Sve'})
    except:
        msg = 'ERROR: Soup Error at  {} \n'.format(str(dt.now()))
        error+=msg
        sendmail(msg,me)
        return
    running = [i.text for i in running]
    new  = running
    print(new)

    # check for any updation in movies
    if testMovie(running):
        body = 'Shit Got Real at {}. Go to the url \n Link : https://paytm.com/movies/allahabad '.format(str(dt.now()))
        sendmail(body,toaddr)
        print("SUCCESS")

    
    prev = deepcopy(running)




def main():
    global error
    st = time.time()
    day = 0
    while True :   
            
        soup  = getSoup()
        findMovie(soup)
        # sleep for  minute. Just being gentle on the server.
        # 1 request per minute
        
        time.sleep(60)
        # get logs via email once in 4 hours just make sure.
        if  time.time() - st > 14400: 
            st = time.time()
            error = 'Day Statistics {} \n {}'.format(', '.join(prev),str(day)) + error
            sendmail(error,me)
            print('Day Statistics {} \n  Day {}:'.format(', '.join(prev),str(day),error)) 
            error = 's'
        
       



prev = ['some_random_shit']
error = ''
message = ''
me = ['mymail@mail.com']
toaddr = ['friend1@mymail.com','friend2@gmail.com']
if __name__ == '__main__':
    main()