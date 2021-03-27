#version that is made with fully my codes + firebase + username + password
import turtle
from datetime import datetime

from newsapi import NewsApiClient
import calendar
from firebase import Firebase

newsapi = NewsApiClient(api_key = 'c6d77cafe721436fa457335fe726f405')

#database to sotre the data of calendar
config = {
    "apiKey": "AIzaSyBvg6CC4Mn0nMP-iCNiqkqg50pWD193YDo",
    "authDomain": "calendar-64c8b.firebaseapp.com",
    "databaseURL": "https://calendar-64c8b-default-rtdb.firebaseio.com",
    "storageBucket": "calendar-64c8b.appspot.com",
}

firebase = Firebase(config)
db = firebase.database()



#basic settings and lists to be used + variables to start off with
pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)

pen2 = turtle.Turtle()
pen2.hideturtle()
pen2.speed(0)

scn = turtle.Screen()
scn.tracer(1000, 0)
user = turtle.Turtle()
user.hideturtle()

now = datetime.now()
current_date = now.strftime("%D").split("/")
current_day = current_date[1]
year = datetime.now().year

import datetime

today = str(datetime.date.today());
today = today.split("-")
tyear = today[0]
xcord = []
ycord = []


#create a list of keys
user_list = []

all_users = db.child("users").get()

for user1 in all_users.each():
    user_list.append(user1.key())


#for retrieving data from online database
def login(nameuser, wordpass):
    if nameuser in user_list:
        if db.child("userinfo").child(nameuser).get().val() == wordpass:
            schedule = db.child("users").child(nameuser).get().val()
            return schedule
        else:
            username2 = input("Username: ")
            wordpass1 = input("Password: ")
            return login(username2, wordpass1)
        
    else:
        db.child("userinfo").child(nameuser).set(wordpass)
        schedule = {}
        return schedule
    
username = input("Username: ")
password = input("Password: ")
scheduledict = login(username, password)




#getting last days of month using calendar
monthday = []
test = calendar.Calendar(firstweekday = 0)
list = []
for month in range(1, 13):
    for day in test.itermonthdays(int(tyear), month):
        list.append(day)
while 0 in list:
    list.remove(0)
start = 0
for i in range(1, len(list)):
    if list[i] == 1:
        monthday.append(list[i - 1])
monthday.append(list[len(list) - 1])


#list for making the calendar
month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

#function to create rectangles
def rec(x, y):
    pen.penup()
    pen.goto(x, y)
    pen.setheading(0)
    pen.pendown()
    for i in range(0, 2):
        pen.forward(30)
        pen.left(90)
        pen.forward(40)
        pen.left(90)

#getting the news title for the day chosen
def changeday(month, day):
    scn.clear()
    if month <= int(current_date[0]) and day <= int(current_day):
        if month < 10:
            month = "0" + str(month)
        if day < 10:
            day = "0" + str(day)
        date = "2021-" + str(month) + "-" + str(day)
        pen.goto(0, 200)
        #allow user to input the keyword and language
        keyword = str(turtle.textinput("keyword", "Enter what you want to search for:"))
        language = str(turtle.textinput("language", "ar, de, en, es, fr, he, it, nl, no, pt, ru, se, ud, zh:"))
        #if the user doesn't input anything
        if language == "None":
            language = "en"
        if keyword == "None":
            keyword = "somethingthatwon'tcomeupwithnewsarticle"
        
        
        pen.write(date, align = "center", font = ("Arial", 15, "normal"))
        all_articles = newsapi.get_everything(q= keyword,
                                          from_param= date,
                                          to= date,
                                          language= language,
                                          sort_by='relevancy')
        print(keyword)
        if len(all_articles["articles"]) >= 5:
#take title and url from the date, newsapi gives data in dictionary format,
#so get tag article, get the index, then print title and url
            for i in range(0, 5):
                title = all_articles["articles"][i]["title"]
                pen.penup()
                pen.goto(0, 190 - 30 * i)
                pen.write(title, align = "center", font = ("Arial", 10, "normal"))
                
                pen.goto(0, 180 - 30 * i)
                url = all_articles["articles"][i]["url"]
                pen.write(url, align = "center", font = ("Arial", 7, "normal"))
                print(title)
                print(url)
        elif len(all_articles["articles"]) <5 and len(all_articles["articles"]) > 0:
            for i in range(0, len(all_articles["articles"]) - 1):
                title = all_articles["articles"][i]["title"]
                pen.penup()
                pen.goto(0, 190 - 30 * i)
                pen.write(title, align = "center", font = ("Arial", 10, "normal"))
                
                pen.goto(0, 180 - 30 * i)
                url = all_articles["articles"][i]["url"]
                pen.write(url, align = "center", font = ("Arial", 7, "normal"))
                print(title)
                print(url)
        else:
            pen.goto(0, 190)
            pen.write("No results", align = "center", font = ("Arial", 10, "normal"))
        
curday = 0
#gets the user to input their schedule        
def addschedule():
    global curday
    global curmon
    
    month = curmon
    day = curday
    date = month, day
    date = str(date)
    
    pen.goto(0, 40)
    pen.write("Your Schedule:", align = "center", font = ("Arial", 15, "normal"))
    
    todo = str(turtle.textinput("Schedule", "For" + str(date) + ":"))
    pen2.clear()
#see if there is already an existing input for the date, if not, append the input with creating a tag, if it exists, don't create tag
    if todo != "None":
        if date in scheduledict.keys():
            scheduledict[date].append(todo)
        else:
            scheduledict[date] = [todo]
        for i in range(0, len(scheduledict[date])):
            pen2.penup()
            pen2.goto(0, 30 - 10 * i)
            pen2.write(scheduledict[date][i], align = "center", font = ("Arial", 10, "normal"))
            
    elif date in scheduledict.keys() and todo == "None":
        for i in range(0, len(scheduledict[date])):
            pen2.penup()
            pen2.goto(0, 30 -10 * i)
            pen2.write(scheduledict[date][i], align = "center", font = ("Arial", 10, "normal"))
        
    elif date not in scheduledict.keys() and todo == "None":
        pen2.goto(0, 30)
        pen2.write("Nothing", align = "center", font = ("Arial", 10, "normal"))
    scn.onkey(addschedule, "a")
    scn.listen()
#list to get the sorted value of distance and the original list of distances        
sortdist = []
unsortdist = []

#function for when clikcked, change screen to the schedule page
def changeclick(x, y):
    global curday
    global curmon
    
    sortdist.clear()
    unsortdist.clear()
    user.penup()
    user.goto(x, y)
    
#for every xcord and ycord, get the distance from the point of click, then get the least of it and get its index to be used for the date
    if x < 110 and x > -110 and y < 130 and y > -20:
        
        for i in range(0, len(xcord)):
            sortdist.append(user.distance(xcord[i], ycord[i]))
            unsortdist.append(user.distance(xcord[i], ycord[i]))
        sortdist.sort()
        curday = unsortdist.index(sortdist[0]) + 1
        
        changeday(curmon, curday)
        addschedule()
        
        scn.onkey(calendar, "b")
        scn.onkey(addschedule, "a")

        scn.listen()
        scn.mainloop()



    
#move calendar back and forth    
def monthpl():
    global curmon
    curmon += 1
    calendar()
  
def monthmi():
    global curmon
    curmon -= 1
    calendar()
 

def exitfunc():
    data = scheduledict
    db.child("users").child(username).set(data)
    quit()

#function making the basic calendar
def calendar():
    scn.tracer(1000, 0)
    global curmon
    monthnumber = curmon
    xcord.clear()
    ycord.clear()

    pen.clear()
    pen2.clear()
    pen2.penup()
    pen2.goto(0, 150)
    pen2.write(month[monthnumber - 1], align = "center")
    for r in range(0, 5):
        days = int(monthday[monthnumber - 1])
        for c in range(0, 7):
            x = r * 7 + c
      
            if days > x:
                pen.color("black")
                rec(-100 + 30 * c, 100 - 40 * r )
                pen.penup()
                #writes the date
                pen.goto(-85 + 30 * c, 120 - 40 * r)
                pen.pendown()
                #xcord and ycord to be used later on to find the date clicked
                xcord.append(pen.xcor())
                ycord.append(pen.ycor())
                if r * 7 + c + 1 == int(current_day) and monthnumber == int(current_date[0]):
                    pen.color("red")
          
                else:
                  pen.color("black")
                pen.write(x + 1, False, align = "center")
                
    scn.onclick(changeclick)
    scn.onkey(monthpl, "Right")
    scn.onkey(monthmi, "Left")
    scn.onkey(exitfunc, "e")
    scn.listen()
#gets the current month
curmon = int(current_date[0])

#runs the function
calendar()
