def findppm():
        import tweepy
        import requests
        from bs4 import BeautifulSoup
        import datetime
        import time
        from datetime import date
        from time import gmtime, strftime

        while True:
                start=time.time()

                url="https://www.esrl.noaa.gov/gmd/ccgg/trends/monthly.html"
                headers={'User-Agent':'Mozilla/5.0'}
                page=requests.get(url)
                soup=BeautifulSoup(page.text, "html.parser")
                #textget=soup.body
                textget=soup.text

                #r=requests.get(url, time.sleep(seconds))
                #textget=r.text

                date=date.today()

                #date2=date.strftime("%b. %-d, %Y")
                # this is the date in the format that co2earth uses (Dec. 16, 2019)
                date2=date.strftime("%B %d:")

                dateyest=date-datetime.timedelta(days=1)
                #date3=dateyest.strftime("%b. %-d, %Y")
                date3=dateyest.strftime("%B %d:")

                dateyestyest=date-datetime.timedelta(days=2)
                #date4=dateyestyest.strftime("%b. %-d, %Y")
                date4=dateyestyest.strftime("%B %d:")

                todaypos=textget.find(date2)
                #print(todaypos)
                yesterdaypos=textget.find(date3)
                #print(yesterdaypos)
                twodaysagopos=textget.find(date4)
                #print(twodaysagopos)

                #if it cant find it then use yesterday
                todaypos=int(todaypos)
                yesterdaypos=int(yesterdaypos)
                twodaysagopos=int(twodaysagopos)

                if todaypos==-1 and yesterdaypos==-1:
                        finddate=twodaysagopos
                        print('No data today or yesterday, this is two days ago:')
                else:
                        if todaypos==-1 and yesterdaypos>0:
                                finddate=yesterdaypos
                                print('No data today, this is yesterday:')
                        else:
                                if todaypos>0:
                                        finddate=todaypos
                                        print('Today data:')
                index1=finddate
                index2=finddate+13
                index3=index2+6
                todayppm=(textget[index2:index3])
                #print(index1)
                print(todayppm)

                # Create variables for each key, secret, token
                consumer_key = 'mOMQ57GwsfK570o8qdgtY1eoB'
                consumer_secret = '3pukKzmJwWqgxV9h2ZS88uny4i90gzJAGlYPja30Aqrad9zj7u'
                access_token = '1212657782589050880-dUrXd0kIwWgEEmR7s6GasdDw9dwZJk'
                access_token_secret = 'a0Cirv6iPBZyng7Q98JOhoRJNkqRr3oZ1I26QvAvGEQoM'

                # Set up OAuth and integrate with API
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token, access_token_secret)
                api = tweepy.API(auth)

                thetime=(strftime("%d/%m/%Y %H:%M:%S", gmtime()))

                # Write a tweet to push to our Twitter account
                words='At '
                words2=', the current atmospheric CO2 concentration is '
                words3='ppm. See you in 12 hours...'
                tweet = words+thetime+words2+todayppm+words3
                api.update_status(status=tweet)
                print(todayppm)
                print(thetime)
                print('tweeted :-)')

                if(todayppm[0].isalpha()) == False:
                        ppm0=todayppm[0]
                        ppm1=todayppm[1]
                        ppm2=todayppm[2]
                        ppm3=todayppm[3]
                        ppm4=todayppm[4]
                        ppm5=todayppm[5]
                else:
                        ppm0=10
                        ppm1=14
                        ppm2=13
                        ppm3=13
                        ppm4=12
                        ppm5=10


           #then set up the display

           # access to GPIO must be through root
                import RPi.GPIO as GPIO
                import time

                LATCH = 16 # CS
                CLK = 15
                dataBit = 11 # DIN

                GPIO.setmode(GPIO.BOARD) #BOARD or BCM
                GPIO.setup(LATCH, GPIO.OUT) # P0
                GPIO.setup(CLK, GPIO.OUT) # P1
                GPIO.setup(dataBit, GPIO.OUT) # P7

           #Setup IO

                GPIO.output(LATCH, 0)
                GPIO.output(CLK, 0)
                def pulseCLK():
                       GPIO.output(CLK, 1)
                       #time.sleep(.001)
                       GPIO.output(CLK, 0)
                       return

                def pulseCS():
                       GPIO.output(LATCH, 1)
                       #time.sleep(.001)
                       GPIO.output(LATCH, 0)
                       return

           # shift byte into MAX7219
           # MSB out first!
                def ssrOut(value):
                       for  x in range(0,8):
                           temp = int(value) & 0x80
                           if temp == 0x80:
                              GPIO.output(dataBit, 1) # data bit HIGH
                           else:
                              GPIO.output(dataBit, 0) # data bit LOW
                           pulseCLK()
                           value = int(value) << 0x01 # shift left
                       return

           # initialize MAX7219 4 digits BCD
                def initMAX7219():
                       # set decode mode
                       ssrOut(0x09) # address
                       #	ssrOut(0x00); // no decode
                       ssrOut(0xFF) # 4-bit BCD decode eight digits
                       pulseCS();

                       # set intensity
                       ssrOut(0x0A) # address
                       ssrOut(0x04) # 9/32s
                       pulseCS()

                       # set scan limit 0-7
                       ssrOut(0x0B); # address
                       ssrOut(0x07) # 8 digits
                       # ssrOut(0x03) # 4 digits
                       pulseCS()

                       # set for normal operation
                       ssrOut(0x0C) # address
                       # ssrOut(0x00); // Off
                       ssrOut(0x01)  # On
                       pulseCS()
                           # clear to all 0s.
                       for x in range(0,9):
                           ssrOut(x)
                           ssrOut(0x0f)
                           pulseCS()
                       return

                def writeMAX7219(data, location):
                       ssrOut(location)
                       ssrOut(data)
                       pulseCS()
                       return


                def displayOff():
                      # set for normal operation
                       ssrOut(0x0C) # address
                       ssrOut(0x00); # Off
                       # ssrOut(0x01)  # On
                       pulseCS()

                def displayOn():
                      # set for normal operation
                       ssrOut(0x0C) # address
                       # ssrOut(0x00); # Off
                       ssrOut(0x01)  # On
                       pulseCS()

                #then show the value on the display

                initMAX7219()

           # in here we need the input of a switch or something
           # if (pin) is high then i=50
           # if pin is low then i = 1202

                for i in range(0,43200):
                      if i<25:
                #this bit says help
                #reduce the 50 above or change all nums to 15 to remove
                         num1=15
                         num2=15
                         num3=12
                         num4=11
                         num5=13
                         num6=14
                         num7=15
                         num8=15 
                         for k in range (1,9):
                            writeMAX7219(num1,8)
                            writeMAX7219(num2,7)
                            writeMAX7219(num3,6)
                            writeMAX7219(num4,5)
                            writeMAX7219(num5,4)
                            writeMAX7219(num6,3)
                            writeMAX7219(num7,2)
                            writeMAX7219(num8,1)
                      else:
                         num1=15
                         num2=ppm0
                         num3=ppm1
                         num4=ppm2
                         num5=10
                         num6=ppm4
                         num7=ppm5
                         num8=15
                      for k in range (1,9):
                            writeMAX7219(num1,8)
                            writeMAX7219(num2,7)
                            writeMAX7219(num3,6)
                            writeMAX7219(num4,5)
                            writeMAX7219(num5,4)
                            writeMAX7219(num6,3)
                            writeMAX7219(num7,2)
                            writeMAX7219(num8,1)
                #displayOff()

           #exit()

           #10 is -
           #11 is E
           #12 is H
           #13 is L
           #14 is P
           #15 is (blank)
           #call("sudo shutdown -h now", shell=True)


                time.sleep(21600)
                #43200=12hrs
