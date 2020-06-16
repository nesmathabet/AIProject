import math
import csv
from datetime import date, timedelta


#To get range of days
#If firstday is "fri" & secondday is "mon"
#Then the output will be ['fri', 'sat', 'sun', 'mon']
def range_days(listt):
   #listt = ["sun","tue"]
   days = ["sat","sun","mon","tue","wed","thu","fri","sat","sun","mon","tue","wed","thu"]
   c = []
   i = 0
   while(i<len(days)):
       if days[i] == listt[0]:
           c.append(days[i])
           i = i + 1
           while( i < len(days)):
               if days[i] != listt[1]:
                   c.append(days[i])
               if days[i] == listt[1]:
                   c.append(days[i])
                   break
               else:
                   i = i + 1
           else:
               c.append(days[i])
           break
       else:
           i = i + 1
   return c

#To calculate the time between two flights(It is used to calculate the G(n)
def calculate_time(day1,time1,day2,time2):
    if day1 == 0 or day2 == 0:
        time = 0
        return time
        
    alldays = ["sat","sun","mon","tue","wed","thu","fri","sat","sun","mon","tue","wed","thu"]
    days = ["fri","sat","sun","mon","tue","wed","thu"]
    if day1 != "fri":
        ManyDays = alldays.index(day2) - alldays.index(day1)
        t1 = time1.split(":")
        t2 = time2.split(":")
        A1 = int(t1[0])
        A2 = int(t1[1])
        B1 = int(t2[0])
        B2 = int(t2[1])
        hours = B1 - A1
        minutes = B2 - A2
        time = abs(hours+(minutes/60)+(ManyDays*24))
        return time
    if day1 == "fri":
        ManyDays = days.index(day2) - days.index(day1)
        t1 = time1.split(":")
        t2 = time2.split(":")
        A1 = int(t1[0])
        A2 = int(t1[1])
        B1 = int(t2[0])
        B2 = int(t2[1])
        hours = B1 - A1
        minutes = B2 - A2
        time = abs(hours+(minutes/60)+(ManyDays*24))
        return time

#print(calculate_time("wed","19:30","wed","7:30"))
#print(calculate_time("thu","23:00","fri","5:00"))
    

#Return one day after the range
def onedaymore(listt):
    alldays = ["sat","sun","mon","tue","wed","thu","fri","sat","sun","mon","tue","wed","thu"]
    days = range_days(listt)
    lastday = days[(len(days)-1)]
    for i in alldays:
        if i == lastday:
            x = alldays.index(lastday)
            days.append(alldays[x+1])
            break
    return days

#print(onedaymore(["fri","tue"]))

#boolean function where first time is greater than the secoond
def first_is_long_time(time1,time2):
    t1 = time1.split(":")
    t2 = time2.split(":")
    A1 = int(t1[0])
    A2 = int(t1[1])
    B1 = int(t2[0])
    B2 = int(t2[1])
    if ( (A1>B1) or ((A1==B1) and (A2>=B2)) ):
         return True
    else:
        return False
#print(first_is_long_time("19:00","7:30"))
      
#To compare two dates, it will return true if day1 and time 1 is more than day2 and time2
def compare_dates(day1,time1,day2,time2):
    alldays = ["sat","sun","mon","tue","wed","thu","fri"]
    if(day1 == 0):
       return False
    if(alldays.index(day1)>alldays.index(day2)):
       return True
    if(alldays.index(day1) == alldays.index(day2)):
        t1 = time1.split(":")
        t2 = time2.split(":")
        A1 = int(t1[0])
        A2 = int(t1[1])
        B1 = int(t2[0])
        B2 = int(t2[1])
        if ( (A1>B1) or ((A1==B1) and (A2>=B2)) ):
            return True
    return False
#print(compare_dates("sat","18:00","sun","12:00"))

#To get the longitude and latitude of a certain city from file --> "Cities.txt"
def get_lon_lat_city(city,filename):
    with open(filename, 'rt') as f:
        csv_reader = csv.reader(f, skipinitialspace=True)
        for line in csv_reader:
            if line[0] == city:
                return [line[1],line[2]]
                break
            else:
                continue
            
#To get the distance between 2 cities            
def get_distance(city1 , city2 , filename):
    R = 6373.0   #radius of the Earth
    list_city1 = []
    list_city2 = []
    #To get the longitude and latitude of the cities
    list_city1 =  get_lon_lat_city(city1,filename)
    list_city2 =  get_lon_lat_city(city2,filename)
     # cordinates
    lat1 = math.radians(float(list_city1[0]))    
    lon1 = math.radians(float(list_city1[1]))
    lat2 = math.radians(float(list_city2[0]))
    lon2 = math.radians(float(list_city2[1]))
    
    # change in coordinates
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2 
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance
#print(get_distance("Aswan","Alexandria","Cities.txt"))
#print(get_distance("Cairo","Shanghai","Cities.txt"))

#The heuristic function is to calculate distance from certain city to the destination city(GOAL)
def get_heuristic(city , goal ,filename):
    r = get_distance(city , goal,filename)
    return r

#To get the days of a filght of a certain flight number
def flightdays(flightnumber,filename):
    with open(filename, 'rt') as f:
        mylines=[]
        csv_reader = csv.reader(f, skipinitialspace=True)
        for line in csv_reader:
            mylines.append(line)
        days = []
        i =0
        while(i< len(mylines)):
            if(mylines[i][4]==flightnumber):
                days = mylines[i][5:10]
                return days
            else:
                i = i + 1
        
  
#To get all the cities that have flights from the input city (and separate their days)
def get_flights(city,filename):
    with open(filename, 'rt') as f:
        mylines=[]
        csv_reader = csv.reader(f, skipinitialspace=True)
        for line in csv_reader:
                mylines.append(line)
        flight = []
        i = 0
        while (i < len(mylines)):
            if(mylines[i][0]== city):
                days = flightdays(mylines[i][4],filename)
                for k in days:
                    s = mylines[i][0:5]
                    s.append(k)
                    flight.append(s)
            i = i + 1
        
        return flight
#print(get_flights("Cairo","Flights.txt"))

#These two functions is to sort the flights by day
def sortdays(listt):
    days = ["sat","sun","mon","tue","wed","thu","fri"]
    return((days.index(listt[5])))
   
def list_days(city,filename):
   listt = []
   listt = get_flights(city,filename)
   listt.sort(key=sortdays)
   return listt
#print(list_days("Cairo","Flights.txt"))
#print((list_days("Milan","Flights.txt")))

#This function to get the flights from the input city where day of flight with in the range and compare_dates is true
def get_children(city,daysflight,day,time,filename):
    result = []
    f = list_days(city,filename)
    #f = get_flights(city,filename)
    i = 0
    while (i < len(f)):  
        if((day in daysflight) and (f[i][5] in daysflight) and (compare_dates(f[i][5],f[i][2],day,time)) and (city == f[i][0])):
                    result.append(f[i])
        i = i + 1
    return result


#print(get_children("New York",["sun","mon"],"sun","7:30","Flights.txt"))
               
               
    




