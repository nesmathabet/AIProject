from Heuristic import get_distance
from Heuristic import get_lon_lat_city
from Heuristic import get_heuristic
from Heuristic import get_children
from Heuristic import range_days
from Heuristic import onedaymore
from Heuristic import calculate_time
from Heuristic import compare_dates
from Heuristic import first_is_long_time
from datetime import date, timedelta
import csv

#To functions to sort the Open List where the least total cost will be found at the end
def takeF(listt):
    return listt[7]
def sortLeastF(listt):
    listt.sort(key=takeF)
    l = listt.reverse()
    return listt

#Function to check if the children is found in OpenList with lower F(n) then don't add it
def addlist(listt,child):
    i = 0 
    while(i<len(listt)):
        if(child[0] == listt[i][0] and child[1] == listt[i][1] and child[7] > listt[i][7]):
            return False
        else:
            i = i+1
    return True


#This Function to choose a list from OpenList
def choose_open(OpenList,ClosedList,rangedays):
    if(len(ClosedList)==0 and len(OpenList) == 1):
        current = OpenList.pop()
        ClosedList.append(current)
        return [OpenList,ClosedList,current]
        exit
    if(len(ClosedList)==1 and len(OpenList)>1):
        current = OpenList.pop()
        ClosedList.append(current)
        return [OpenList,ClosedList,current]
        exit 
    if(len(ClosedList)>1):
        LastClosedindex = len(ClosedList) - 1
        LastClosed = ClosedList[LastClosedindex]
        n = len(OpenList)-1
        while(n>0):
            # the date and departure time of the next flight should be more than the date and arrival time of previous flight
            if( (compare_dates(OpenList[n][5],OpenList[n][2],LastClosed[5],LastClosed[3])== True)):
                current = OpenList.pop(n)
                ClosedList.append(current)
                break
                
            else:
                n = n - 1
        return [OpenList,ClosedList,current]
        exit
        
        
#The main A search algorithm
def ASearch(start,goal,listofdays):
    #To get the list of valid days
    days = range_days(listofdays)
    ClosedList = []
    #The list consist of [start,destination,departure,arrival,day,g(n),f(n)]
    OpenList = [[0,start,"0:00","0:00",0,0,0,0]]
    #while open list is not empty
    while (len(OpenList) >0):
        #To sort the openlist where the least f(n) found at the end
        OpenList = sortLeastF(OpenList)
        
        #current = OpenList.pop()
        #ClosedList.append(current)
        #Call function choose_open to choose the suitable list
        choose = choose_open(OpenList,ClosedList,days)
        OpenList = choose[0]
        ClosedList = choose[1]
        current = choose[2]
        
        #If the destination of current list is the goal then end
        if (current[1] == goal):
            return ClosedList
            break
        day = days[0]
        time = "00:00"
        city = current[1]
        alldays=["sat","sun","mon","tue","wed","thu","fri"]
        # If the destination is not the start
        if (current[1] != start ):
               closedindex = len(ClosedList)-1
               Last = ClosedList[closedindex]
               city = Last[1]
               time = Last[3]
               # If the day ends where the departure time will be greater than the arrival time 
               if((first_is_long_time(Last[2],Last[3]))== True):
                   indexdays = alldays.index(Last[5])
                   # If the day is not friday
                   if (indexdays != 6):
                       day = alldays[indexdays+1]
                   # If the day is friday then the next day is saturday
                   else:
                       day = alldays[0]
               else:
                   # If arrival is greater than departure time then return the last day
                   day = Last[5]
        #While get children returns empty list
        while(get_children(city,days,day,time,"Flights.txt") == []):
            # remove the last list in closed list
            ClosedList.pop(len(ClosedList)-1)
            # save the new last list from Closedlist in "Last" 
            lastindex = len(ClosedList)-1
            Last = ClosedList[lastindex]
            # choose another list from open list 
            choose = choose_open(OpenList,ClosedList,days)
            OpenList = choose[0]
            ClosedList = choose[1]
            current = choose[2]
            city = current[1]
            time = current[3]
            # If we didn't return to the start list
            if (Last[1] != start and len(ClosedList)!=1 ):
                if((first_is_long_time(Last[2],Last[3]))):
                    indexdays = alldays.index(Last[5])
                    if (indexdays != 6):
                        day = alldays[indexdays+1]
                    else:
                        day = alldays[0]
                else:
                    day = Last[5]
            else:
                city = current[1]
                day = current[5]
                time =current[3]
            
            
        #All childrens 
        childrens = get_children(city,days,day,time,"Flights.txt")
        i = 0
        o = []
        while(i<len(childrens)):
            # To check if the the children was in closed list
            if ((childrens[i] in ClosedList)):
                continue
            # To check if ClosedList have more than one element 
            if(len(ClosedList) > 1):
                #Get the g(n)
                G = current[6] +  calculate_time(childrens[i][5],childrens[i][2],current[5],current[3])
                #Get the h(n)
                H = get_heuristic(childrens[i][1],goal,"Cities.txt")
                #Get the final cost 
                F = G + H
                s = [G,F]
                #Add G(n) and F(n) to the children's list
                x = childrens[i].extend(s)
                o = childrens[i]
                # If it is valid to add it then add child to open list
                if(addlist(OpenList,o)):
                    OpenList.append(o)
            #If the Closed List has only one element   
            if(len(ClosedList) == 1):
                #Calculate time will be the time from departure till time of arrival
                #Get the g(n)
                G = current[6] + calculate_time(childrens[i][5],childrens[i][2],childrens[i][5],childrens[i][3])
                #Get the h(n)
                H = get_heuristic(childrens[i][1],goal,"Cities.txt")
                F = G + H
                s = [G,F]
                #Add G(n) and F(n) to the children's list
                x = childrens[i].extend(s)
                o = childrens[i]
                # If it is valid to add it then add child to open list
                if(addlist(OpenList,o)):
                    OpenList.append(o)
            i = i + 1
           
    return None
            

def main():
    while (True):
        start = input("Please enter the Source city \n")
        end = input("Please enter the Destination city \n")
        if( start == end):
            print("Enter different destination")
            continue
        FDay = input("Enter the first day in range of days like (sun,mon,tue,...,fri) \n")
        LDay = input("Enter the last day in range of days like (sun,mon,tue,...,fri) \n")
        if( start == end):
            print("Enter different destination")
        listt1 = []
        listt1.append(FDay)
        listt1.append(LDay)
        result = ASearch(start,end,listt1)
        if(result == None):
            list2 = onedaymore(listt1)
            result2 = ASearch(str(start),str(end),list2)
            if (result2 == None):
                print("No available flights")
        if(result != None):
            count = 1
            i = 0
            for l in result:
                if( i ==0):
                    i = i + 1
                    continue
                if(i > 0):
                    print("Step",count,":","Use flight",l[4],"from",l[0],"to",l[1],"departure time at",l[2],"arrival time at",l[3],"on",l[5])
                    count = count + 1
                    i = i + 1
                
main()            
