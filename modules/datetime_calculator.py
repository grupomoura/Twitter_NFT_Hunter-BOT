from datetime import datetime

def getDifference(then, now = datetime.now(), interval = "mins"):

    now = datetime.now()
    duration = now - then
    duration_in_s = duration.total_seconds() 
    
    #Date and Time constants
    yr_ct = 365 * 24 * 60 * 60 #31536000
    day_ct = 24 * 60 * 60 			#86400
    hour_ct = 60 * 60 					#3600
    minute_ct = 60 
    
    def yrs():
      return divmod(duration_in_s, yr_ct)[0]

    def days():
      return divmod(duration_in_s, day_ct)[0]

    def hrs():
      return divmod(duration_in_s, hour_ct)[0]

    def mins():
      return divmod(duration_in_s, minute_ct)[0]

    def secs(): 
      return duration_in_s

    return {
        'yrs': int(yrs()),
        'days': int(days()),
        'hrs': int(hrs()),
        'mins': int(mins()),
        'secs': int(secs())
    }[interval]


# then = datetime(1987, 12, 30, 17, 50, 14) #yr, mo, day, hr, min, sec
# now = datetime(2020, 12, 25, 23, 13, 0)

# print('The difference in seconds:', getDifference(then, now, 'secs'))  
# print('The difference in minutes:', getDifference(then, now, 'mins'))
# print('The difference in hours:', getDifference(then, now, 'hrs'))     
# print('The difference in days:', getDifference(then, now, 'days'))   
# print('The difference in years:', getDifference(then, now, 'yrs'))