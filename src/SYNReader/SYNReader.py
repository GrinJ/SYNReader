import re

class SYNReader:

    def __init__(self, filename):
        """
        Allow to read files of meteorological observations (SYNOPMAK or SYNOPDOP).

        To work with the class, specify the path to the data file

        :param filename: path to the file
        :type filename: basestring
        """

        #Dictionary with keys
        self.keys = ["dist_num", "st_num", "lat", "lon", "heigth", "PR", "HH", "Pz", "P0", "t", "td", "dd", "ff", "L",
                     "q", "VV", "SS", "N", "Nh", "Cl", "Cm", "Ch", "hh", "ww", "W", "t_min", "t_max", "tgm", "R6", "R12",
                     "R24", "tg", "hhs", "mv", "E4", "E1", "E3", "Sp1", "Sp2", "Sp3", "P01", "P0gk", "P0p", "t_gk", "t_p", "t_0"]

        #Flag of successful file open
        self.noProblem = True

        try:
            #Open the file
            file = open(filename, 'r')
            values = file.read().split("\n")

            #Create custom dict to save the data
            self.data = {}

            #Create empty tuples
            for key in self.keys:
                self.data[key] = []

            #For loop counter
            self.counter = 0

            #Read the data
            for key in values:
                value = re.findall(r"[-+]?\d*\.\d+|\d+", key)
                if len(value) > 0:
                    if float(value[0]) == 22222.0:
                        break
                    if len(value) == 46:
                        count = 0
                        for subkey in value:
                            if subkey != "":
                                self.data[self.keys[count]].append(float(subkey))
                                count += 1
                        self.counter += 1

            #If file was empty
            if self.counter == 0:
                self.noProblem = False
                return

        except IOError:
            self.noProblem = False

    def convertData(self, keys=[]):
        """
        Converts data values from the SYN specification to normal values
        """

        #Check if given value was empty
        if keys == []:
            keys = self.keys

        #Loop throug all data
        for key in keys:
            for num in range(0, self.data[key].__len__()):
                if self.data[key][num] != -9999.0:
                    self.data[key][num] = self.__convert(key, self.data[key][num])

    #Returns converted value for the key
    def __convert(self, key, value):
        return {
            "lat": value / 100.0,
            "lon": value / 100.0,
            "Pz": value / 10.0,
            "P0": value / 10.0,
            "t": (value - 1000.0) / 10.0,
            "td": (value - 1000.0) / 10.0,
            "q": (value - 1000.0) / 10.0,
            "VV": value / 10.0,
            "SS": value / 10.0,
            "t_min": (value - 1000.0) / 10.0,
            "t_max": (value - 1000.0) / 10.0,
            "tgm": (value - 1000.0) / 10.0,
            "R6": value / 10.0,
            "R12": value / 10.0,
            "R24": value / 10.0,
            "tg": (value - 1000.0) / 10.0,
            "P01": value / 10.0,
            "P0gk": value / 10.0,
            "P0p": value / 10.0,
            "t_gk": value / 10,
            "t_p": value / 10,
            "t_0": value / 10,
        }.get(key, value)


    #Check if values is or not empty
    def isNull(self, values, num):
        """
        Checks if value not equal to zero of the parameter from the station.

        :param values: list of the keys
        :type values: tuple
        :param num: number in the list in range(0, counter)
        :type num: int
        :return: False if not empty
        :rtype: bool
        """

        #Local counter
        count = 0

        #Loop throug all arguments
        for value in values:
            if self.data[value][num] != -9999.0:
                count += 1

        #Check the value of out counter
        if values.__len__() == count:
            return False
        else:
            return True

    #Returns the array bt given key
    def __getitem__(self, item):
        return self.data[item]

    def inArea(self, minLat, maxLat, minLon, maxLon):

        """
        Returns an array of indices of points that are in the given area
        :param minLat: The minimum latitude value
        :type minLat: float
        :param maxLat: The maximum latitude value
        :type maxLat: float
        :param minLon: The minimum longitude value
        :type minLon: float
        :param maxLon: The maximum longitude value
        :type maxLon: float
        :return: Array of indices
        :rtype: tuple
        """

        #Value that will be returned
        tmp =[]

        # Loop through all the station data
        for st in range(0, self.counter):

            #Add index if point is in area
            if self.data["lat"][st] >= minLat and self.data["lat"][st] <= maxLat and \
                self.data["lon"][st] >= minLon and self.data["lon"][st] <= maxLon:
                tmp.append(st)

        #Return the tuple with indecies
        return tmp