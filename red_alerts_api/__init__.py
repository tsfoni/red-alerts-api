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
RED_ALERT_JSON_TITLE = "ירי טילים ורקטות"

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
            
            if len(alerts_content) == ALERTS_EMPTY_LENGTH:
                return None

            alerts_content = "{\"alerts\":[" + alerts_content[1:-1] + "}"
            all_alerts = self.encode_json_to_objects(json.loads(alerts_content))
        except Exception as e:
            return e     

        new_alerts = []
        for alert in all_alerts:
            if cmp_alerts(alert, self.__last_alert):
                break
            new_alerts.append(alert)
            
        self.__last_alert = all_alerts[0] # Updating last alert.

        return new_alerts

    def encode_json_to_objects(self, alerts_json) -> list:
        """
        Converting all alerts from json file and turning them to list of 'alert' objects.
        Reutrn:
            list of alert objects
        """
        all_alerts = []
        for each_alert in alerts_json["alerts"]:
            if each_alert["title"] == RED_ALERT_JSON_TITLE: # Filters only red 
                all_alerts.append(alert(each_alert["data"], datetime.strptime(each_alert["alertDate"], PIKUD_DATETIME_FORMAT))) # New 'alert' object
        
        return all_alerts