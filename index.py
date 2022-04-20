# Example of red alerts api usage.

import red_alerts_api as r
import time

alerts = r.red_alerts()
while True: 
    new_alerts = alerts.get_new_alerts()
    if new_alerts != None:
            for new_alert in new_alerts:
                print(new_alert.__str__())
    time.sleep(4)