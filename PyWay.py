import urllib2

class createInterface:

    def __init__(self):

        self.cachedStops = {}
        self.cachedSchedules = {}

    def __parseStopData__(self, rawdata, cache):

        parsedData = {}

        for stop in rawdata:
            parsedData[stop[0:4]] = stop[7:len(stop)]

            if cache == True:
                self.cachedStops[stop[0:4]] = stop[7:len(stop)]

        return parsedData

    def __parseTimeData__(self,rawdata):

        passingTimes = []

        for n in xrange(len(rawdata)):
            k = 0
            if rawdata[n] == "A" or rawdata[n] == "P":
                if rawdata[n+1] == "M":
                    while rawdata[n-k] != ">":
                        k += 1
                    passingTimes.append(rawdata[n-k+1:n]+rawdata[n]+rawdata[n+1])

        return passingTimes

    def createID(self, stop, route, direction):
        return str(stop) + ':' + str(route) + ':' + direction

    def getRouteStops(self, route, direction, format="parsed", cache=True):

        key = str(route) + '_' + direction

        info = urllib2.urlopen('http://m.miway.ca/routeStops.jsp?id=' + key)
        data = ' '.join(info.read().split())
        line = data[data.index('</h4>'):len(data)]

        rawdata = []

        while True:
            try:
                stop = line[line.index(key + '">')+len(key)+2:line.index('</a>')]
                rawdata.append(stop)
                line = line[line.index(stop) + len(stop)+ 10:len(line)]
            except ValueError:
                break

        if(format == "parsed"):
            return self.__parseStopData__(rawdata,cache)
        else:
            return rawdata

    def getNextPassingTime(self, stop, route, direction):

        info = urllib2.urlopen('http://m.miway.ca/nextPassingTimes.jsp?sId=' + str(stop) + '&id=' + str(route) + '_' + direction)
        data = ''.join(info.read().split())
        line = data[data.index('<tdcolspan="2"NOWRAP><b/>'):data.index('<tdcolspan="2"><ahref=')]

        return self.__parseTimeData__(line)

    def getFullSchedule(self, stop, route, direction, cache=True, day="AUTO"):

        days = {"MONDAY":"1", "TUESDAY":"1", "WEDNESDAY":"1", "THURSDAY":"1", "FRIDAY":"1", "SATURDAY":"2", "SUNDAY":"3", "HOLIDAY":"3"}

        if day == "AUTO":
            info = urllib2.urlopen('http://m.miway.ca/fullSchedule.jsp?sId=' + str(stop) + '&id=' + str(route) + '_' + direction)
        else:
            info = urllib2.urlopen('http://m.miway.ca/fullSchedule.jsp?wkd=' + days[day.upper()] + "&sId=" + str(stop) + '&id=' + str(route) + '_' + direction)

        data = ''.join(info.read().split())
        line = data[data.index("fullSchedule"):data.index("</td></tr></table></tr>")]

        fullSchedule = self.__parseTimeData__(line)

        if cache == True:
            self.cachedSchedules[str(stop) + ':' + str(route) + ':' + direction] = fullSchedule

        return fullSchedule
