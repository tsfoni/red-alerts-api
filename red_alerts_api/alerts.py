"""
Alerts Module
~~~~~~~~~~~~~~~~~~~~~
Module with functions and classes needed for alert handling/creating
"""

from datetime import datetime

class alert:
    """
    Alert Class
    ~~~~~~~~~~~~~~~~~~~~~
    Simple class with needed members and methods for alert.
    """

    def __init__(self, city: str, time: datetime) -> None:
        self.__city = city
        self.__time = time

    def get_city(self) -> str:
        return self.__city
    
    def get_time(self) -> datetime:
        return self.__time
    
    def __str__(self) -> str:
        return F"City: {self.__city}, Time: {self.__time}"
    