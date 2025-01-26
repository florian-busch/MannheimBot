import requests
from datetime import datetime

def constructDateForQuery(day):
        today = datetime.now()
        date = f"isodate%3A%22{str(today.year)}%2F{str(today.month)}%2F{str(today.day - day)}%22"
        return date

def queryBuilder(location, day):
        return f"https://mannheim.opendatasoft.com/api/explore/v2.1/catalog/datasets/{location}/records?limit=100&refine={constructDateForQuery(day)}"

def fetchBikeData(location, day):
        query = queryBuilder(location, day)
        #get data from mannheim.opendatasoft.com and turn it into json
        fetched_data = requests.get(query).json()
        return fetched_data


