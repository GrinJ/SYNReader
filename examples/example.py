from src.SYNReader.SYNReader import SYNReader

#Create object
syn = SYNReader('./examples/data/SYN_2015081721.txt')

#Check if file was successfully opened and readed
if syn.noProblem:

    #Formate the data if it is needed
    syn.convertData()

    #For example - calculate relative humidity
    RH = []

    #Loop throug all values
    for i in range(0, syn.counter):
        #Check the correct value of t and td parametrs
        if not syn.isNull(["t", "td"], i):
            RH.append(100.0 - 5.0 * (syn.data["t"][i] - syn.data["td"][i]))

    #For example - print the output result
    print(RH)
else:
    #Catch the error
    print("error happened")