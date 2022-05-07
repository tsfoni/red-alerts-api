# Example of red alerts api usage.

import red_alerts_api as r
import time

alerts = r.red_alerts()
while True: 
    new_alerts = alerts.get_new_alerts()
    for new_alert in new_alerts:
        print(new_alert.__str__())
    print("New round.")
    time.sleep(1)
