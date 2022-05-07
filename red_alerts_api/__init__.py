"""
This module does red alerts handling.
***Dont work within Israel!***
"""

if __name__ == "__main__":
    raise Exception("You shouldn't run this file.")

from datetime import datetime
import requests, json
from .alerts import alert, cmp_alerts

ALERTS_URL = "https://www.oref.org.il/WarningMessages/History/AlertsHistory.json"
PIKUD_DATETIME_FORMAT = r"%Y-%m-%d %H:%M:%S"
ALERTS_EMPTY_LENGTH = 2 # Length of empty alerts list.

class red_alerts:
    def __init__(self) -> None:
        self.__last_alert = alert("", datetime(1879, 3, 14, 11, 30, 0))

    def get_new_alerts(self) -> list:
        """
        Return:
            list of unreaded 'alert' objects, else None
        """
        try:            
            alerts_content = str(requests.get(ALERTS_URL).content, encoding='utf8')
            # alerts_content = ''.join(open("AlertsHistory.json", 'r').readlines()) #<-- for self testing with local file
            
            if len(alerts_content) <= ALERTS_EMPTY_LENGTH:
                return None

            alerts_content = "{\"alerts\":" + alerts_content[alerts_content.index("["):
                                                            alerts_content.index("]")] + "]}"
            all_alerts = red_alerts.__encode_json_to_objects(json.loads(alerts_content))
        except Exception as e:
            raise e     

        new_alerts = []
        for each_alert in all_alerts:
            if cmp_alerts(each_alert, self.__last_alert):
                break
            new_alerts.append(each_alert)
            
        self.__last_alert = all_alerts[0] # Updating last alert.

        return new_alerts

    def __encode_json_to_objects(alerts_json) -> list:
        """
        Converting all alerts from json file and turning them to list of 'alert' objects.
        Reutrn:
            list of alert objects
        """
        all_alerts = []
        for each_alert in alerts_json["alerts"]:
            time = datetime.strptime(each_alert["alertDate"], PIKUD_DATETIME_FORMAT)    
            
            # Inside one alert could be more than 1 city, this will separate each city to its own 'alert' object.
            cities = each_alert["data"].split(', ')
            for city in cities:
                all_alerts.append(alert(city, time))

        return all_alerts

