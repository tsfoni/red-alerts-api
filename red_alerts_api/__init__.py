"""
This module does red alerts handling.
"""

if __name__ == "__main__":
    raise Exception("You shouldn't run this file.")

from datetime import datetime
import requests, json
from .alerts import alert

ALERTS_URL = "https://www.oref.org.il/WarningMessages/History/AlertsHistory.json"
PIKUD_DATETIME_FORMAT = r"%Y-%m-%d %H:%M:%S"

class red_alerts:
    def __init__(self) -> None:
        self.__last_alert = alert("", datetime(1879, 3, 14, 11, 30, 0))

    def get_all_alerts(self) -> list:
        """
        Return:
            List(alert) of all alerts in the current day.
        """
        try:            
            alerts_content = str(requests.get(ALERTS_URL).content, encoding='utf8')
            # alerts_content = ''.join(open("AlertsHistory.json", 'r').readlines()) #<-- for self testing with local file
            
            if len(alerts_content) <= 2: # Length of empty alerts list.
                return []

            alerts_content = "{\"alerts\":" + alerts_content[alerts_content.index("["):
                                                            alerts_content.index("]")] + "]}"
            all_alerts = red_alerts.__encode_json_to_objects(json.loads(alerts_content))
        except Exception as e:
            raise e     

        return all_alerts


    def get_new_alerts(self) -> list:
        """
        Return:
            List(alert) of unreaded alerts in the current day.
        """
        all_alerts = self.get_all_alerts()
        if len(all_alerts) == 0: 
            return all_alerts # Empty list.

        new_alerts = []
        for each_alert in all_alerts:
            if each_alert.__str__() == self.__last_alert.__str__():
                break
            new_alerts.append(each_alert)

        self.__last_alert = all_alerts[0] # Updating last alert.

        return new_alerts


    def __encode_json_to_objects(alerts_json) -> list:
        """
        Converting all alerts from json file format and turning them to list of 'alert' objects.
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

