import re
from dateutil import parser
class Utils(object):
    @staticmethod
    def validateISO8601Date(strDate):
        regex = r"^(?:[1-9]\d{3}-(?:(?:0[1-9]|1[0-2])-(?:0[1-9]|1\d|2[0-8])|(?:0[13-9]|1[0-2])-(?:29|30)|(?:0[13578]|1[02])-31)|(?:[1-9]\d(?:0[48]|[2468][048]|[13579][26])|(?:[2468][048]|[13579][26])00)-02-29)T(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d(?:Z|[+-][01]\d:[0-5]\d)$"
        try:
            pattern = re.compile(regex)
        except re.error:
            print("Non valid pattern for time validation, please test your regex")
            exit()  
        return re.fullmatch(pattern, strDate) != None
    @staticmethod
    def isFridayRush(strDate):
        date = parser.parse(strDate)
        return date.weekday() == 4 and date.hour >= 15 and date.hour <= 19
if(__name__=="__main__"):
    print(Utils.validateISO8601Date("2021-01-16T13:00:00Z"))