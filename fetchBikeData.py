import requests
from datetime import datetime, timedelta, date

def constructDateForQuery(daysBackwards):
        pastDate = str(date.today() - timedelta(days = daysBackwards))
        splittedDate = pastDate.split("-")
        return f"isodate%3A%22{str(splittedDate[0])}%2F{str(splittedDate[1])}%2F{str(splittedDate[2])}%22"

def buildQuery(location, daysBackwards):
        return f"https://mannheim.opendatasoft.com/api/explore/v2.1/catalog/datasets/{location}/records?limit=100&refine={constructDateForQuery(daysBackwards)}"

def fetchBikeData(location, daysBackwards):
        query = buildQuery(location, daysBackwards)
        #get data from mannheim.opendatasoft.com and turn it into json
        fetched_data = requests.get(query).json()
        return fetched_data