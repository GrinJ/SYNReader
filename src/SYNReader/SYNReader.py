from collections import defaultdict
import re
import numpy

class SYNReader:

    def __init__(self, filename):
        """
        Allow to read files of meteorological observations (SYNOPMAK or SYNOPDOP).

        To work with the class, specify the path to the data file

        :param filename: path to the file
        :type filename: basestring
        """

        #Dictionary with keys
        self.keys = {0: "dist_num", 1: "st_num", 2: "lat", 3: "lon", 4: "heigth", 5: "PR", 6: "HH", 7: "Pz", 8: "P0", 9: "t",
         10: "td", 11: "dd", 12: "ff", 13: "L", 14: "q", 15: "VV", 16: "SS", 17: "N", 18: "Nh", 19: "Cl", 20: "Cm", 21: "Ch", 22: "hh",
         23: "ww", 24: "W", 25: "t_min", 26: "t_max", 27: "tgm", 28: "R6", 29: "R12", 30: "R24", 31: "tg", 32: "hhs", 33: "mv",
         34: "E4", 35: "E1", 36: "E3", 37: "Sp1", 38: "Sp2", 39: "Sp3", 40: "P01", 41: "P0gk", 42: "P0p", 43: "t_gk", 44: "t_p", 45: "t_0"}

        #Flag of successful file open
        self.noProblem = True

        try:
            #Open the file
            file = open(filename, 'r')
            values = file.read().split("\n")

            #Create custom dict to save the data
            result = defaultdict(list)
            #self.data = defaultdict(list)
            self.data = {}
            self.__tmp = defaultdict(list)

            #For loop counter
            self.counter = 0

            #Read the data
            for key in values:
                value = re.findall(r"[-+]?\d*\.\d+|\d+", key)
                if float(value[0]) == 22222.0:
                    break
                if value.__len__() == 46:
                    count = 0
                    for subkey in value:
                        if subkey != "":
                            result[self.counter].append(float(subkey))
                            count += 1
                    self.counter += 1

            #If file was empty
            if self.counter == 0:
                self.noProblem = False
                return

            #Work with the data
            for i in range(0, result.__len__()):
                for j in range(0, 45):
                    self.__tmp[self.keys[j]].append(result[i][j])

            #convert list to numpy array
            for j in range(0, 45):
                self.data[self.keys[j]] = numpy.array(self.__tmp[self.keys[j]])

        except IOError:
            self.noProblem = False

    def convertData(self):
        """
        Converts data values from the SYN specification to normal values
        """
        for key, val in self.data.items():
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