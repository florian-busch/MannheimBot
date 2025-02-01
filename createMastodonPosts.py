from fetchBikeData import fetchBikeData
from datetime import date, timedelta
from collections import defaultdict

zaehlstellen_locations = ["renzstr-ost-eco-counter-daten", "renzstr_west_eco-counter-daten", "kurpfalzbrucke_neckarstadt-eco-counter-daten-kopieren", "kurpfalzbrucke_innenstadt-eco-counter-daten", "kurt-schumacher-brucke-sud-hafenstr-eco-counter-daten", "konrad_adenau_bruecke_sued-gesamt-eco-counter-daten", "neckarauer-ubergang-eco-counter-verkehrszahler", "schlosspark-lindenhof-eco-counter-verkehrszahler"]
zaehlstellen_data = defaultdict(dict)
zaehlstellen_location_names = []

def calculatePassedBikeNumbers():
    for location in zaehlstellen_locations:
        counter_two_days_ago = 0
        counter_three_days_ago = 0
        try:
            #fetch bike data from fetchBikeData.py
            data_two_days_ago = fetchBikeData(location, 2)
            data_three_days_ago = fetchBikeData(location, 3)
            
            #create sum of counts from data two days ago and add name and count to zaehlstellenData
            try:
                #go through hourly entries and calculate sum
                for entry in data_two_days_ago.get('results'):
                    if type(entry.get('counts')) == int:
                        counter_two_days_ago += entry["counts"]
                #append {'name': sum} to zaehlstellen_data
                zaehlstellen_data[entry['name']].update({'twoDaysAgo': counter_two_days_ago})
                #append name of zaehlstelle for later iteration
                zaehlstellen_location_names.append(entry['name'])
               
                #calculate difference in passed bikes to day before
                for entry in data_three_days_ago.get('results'):
                    if type(entry.get('counts')) == int:
                        counter_three_days_ago += entry['counts']
                zaehlstellen_data[entry['name']].update({'changeToDayBefore': counter_three_days_ago - counter_two_days_ago})

            except ValueError:
                   print('Error processing data from queryServer')
        except ValueError as e:
            print("Error " + e)


def buildStatus():
    #fill zaehlstellenData and zaehlstellenDataNames with fetched data
    calculatePassedBikeNumbers()
    
    #create empty string which gets filled with content for post
    post = f"Rad-Zählstellen in Mannheim, {str(date.today() - timedelta(days = 2))}.\n"
    
    #access zaehlstellenData-dict via location names from zaehlstellenLocations and add counts to post
    for location in zaehlstellen_location_names:
        change_to_day_before = zaehlstellen_data[location].get('changeToDayBefore')

        post = f"{post}\n{str(location)}: {str(zaehlstellen_data[location].get('twoDaysAgo'))} "
        
        #TO DO: data changes on server after post is done. change to day before therefor not correct. Maybe get data from recent post and calculate off of this?
        #insert change to day before in post. 
        if change_to_day_before == 0:
            post = post + 'Gleich zum Vortag.'
        # changeToDayBefore is negative -> 2 days ago less bikes were counted than 3 days before
        elif change_to_day_before < 0:
            post = post + " (" + '\u2197 ' + str(abs(change_to_day_before)) + ')'
        # changeToDayBefore is positive -> 2 days ago more bikes were counted than 3 days before
        elif change_to_day_before > 0:
            post = post + " (" + '\u2198 ' + str(abs(change_to_day_before)) + ')'
        else:
            post = post + " (??)"
    #add hashtags to post
    post = post + "\n\n#fahrrad #mannheim #verkehrswende"
    

    return post

