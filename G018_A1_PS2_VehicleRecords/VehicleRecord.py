#Opening files all the three files: input, output and prompt
inputFile = open('inputPS2.txt', 'r')
promptFile = open('promptsPS2.txt','r')
outputFile = open('outputPS2.txt', 'w')

#Node structure in terms of class of Truck Node
class TruckNode:
    numOfVariable = 0
    max_limit = 0
    availTruckList = list()
    maxDeliveries = list()
    orderStatus = list()
    UID = list()
    count = list()
    
	#Constructor with UID of Truck 
    def __init__(self, Uid):
        self.left = None
        self.right = None
        self.UId = int(Uid)
        self.chkoutCtr = 0



#This function reads the input file where the data of truck's UID entering & exiting the warhouse is present. It reads the data then accordingly the Binary tree is created. It checks for the UID of the truck and increment the Check_Out_Count variable "chkoutCtr" as per the data received from the input file.
def _readTruckRec(tNode, Uid):
    if tNode is None:
        TruckNode.numOfVariable += 1
        TruckNode.UID.append(Uid)
        TruckNode.count.append(0)
        return TruckNode(Uid)
    else:
        if tNode.UId == Uid:
            tNode.chkoutCtr += 1
            index = TruckNode.UID.index(Uid)
            TruckNode.count[index] = tNode.chkoutCtr
            return tNode
        elif tNode.UId < Uid:
            tNode.right = _readTruckRec(tNode.right, Uid)
        else:
            tNode.left = _readTruckRec(tNode.left, Uid)
    return tNode 




#This function reads the Binary tree and reads its TruckNode. The value of Truck's UID and its chkoutCtr variable is read and then written to the output file. 
def _printTruckRec(tNode):
    if tNode:
        _printTruckRec(tNode.left)
        printLine = str(tNode.UId) + "," + str(tNode.chkoutCtr) + "\n"
        outputFile.write(printLine)
        _printTruckRec(tNode.right)




#This function reads the data from TruckNode and check chkoutCtr value. Accordingly it will print the statement to the output file as per its status in the system of Binary Tree.
def _checkTruckRec(tNode, Uid):
    if tNode:
        if tNode.UId == Uid:
            if (tNode.chkoutCtr % 2 != 0) and (tNode.UId == Uid):
                outputFile.write("Vehicle id "+ str(Uid) +" entered "+ str(tNode.chkoutCtr) +" times into the system. It is currently fulfilling an open order.\n")
            elif (tNode.chkoutCtr % 2 == 0) and (tNode.UId == Uid):
                outputFile.write("Vehicle id "+ str(Uid) +" entered "+ str(tNode.chkoutCtr) +" times into the system. It just completed an order.\n")
            elif (tNode.chkoutCtr == 0) and (tNode.UId == Uid):
                outputFile.write("Vehicle id "+ str(Uid) +" just reached the warehouse.\n")
        elif tNode.UId < Uid:
            _checkTruckRec(tNode.right, Uid)
        else:
            _checkTruckRec(tNode.left, Uid)
    else:
        outputFile.write("Vehicle id "+ str(Uid) +" did not come to the warehouse today.\n")






def _availTrucks(tNode):
    if tNode:
        _availTrucks(tNode.left)
        if (tNode.chkoutCtr == 0):
            TruckNode.availTruckList.append(tNode.UId)
            #print(TruckNode.availTruckList)
        elif (tNode.chkoutCtr%2 == 0) and (tNode.chkoutCtr < TruckNode.max_limit*2):
            TruckNode.availTruckList.append(tNode.UId)
            #print(TruckNode.availTruckList)
        _availTrucks(tNode.right)
    

        


def _highFreqTrucks(tNode, frequency):
    flag = False
    if tNode:
        _highFreqTrucks(tNode.left, frequency)
        if (frequency * 2 <= tNode.chkoutCtr):
            return("Vehicles that moved in/out more than "+ str(frequency) +" times are: \n" + str(tNode.UId) + "," + str(tNode.chkoutCtr) + "\n")
        _highFreqTrucks(tNode.right, frequency)
        

        




def _maxDeliveries(tNode):
    if tNode:
        _maxDeliveries(tNode.left)
        if (tNode.chkoutCtr % TruckNode.max_limit == 0) and (tNode.chkoutCtr >= TruckNode.max_limit*2):
            TruckNode.maxDeliveries.append(tNode.UId)
            #print(TruckNode.maxDeliveries)
        _maxDeliveries(tNode.right)






def _updateTruckRec(tNode, Uid):
    if tNode is None:
        return TruckNode(Uid)
    else:
        if tNode.UId == Uid:
            tNode.chkoutCtr += 1
            return tNode
        elif tNode.UId < Uid:
            tNode.right = _readTruckRec(tNode.right, Uid)
        else:
            tNode.left = _readTruckRec(tNode.left, Uid)
    return tNode 




def _printOrderStatus(targetorders):
    #print(targetorders)
    #print("UID list: ",TruckNode.UID)
    #print("count list: ", TruckNode.count)
    o = [0]*3
    yet = 0
    openn = 1 
    closed = 2
    for i in TruckNode.count:
        if i % 2 == 0:
            o[closed] += (i / TruckNode.max_limit)
        elif i % 2 != 0:
            o[openn] += 1
    o[yet] = targetorders - o[closed] - o[openn]
    #print(o)
    outputFile.write("Open Orders: "+ str(int(o[openn])) + "\n")
    outputFile.write("Closed Orders: "+ str(int(o[closed])) + "\n")
    outputFile.write("Yet to be fulfilled: "+ str(int(o[yet])) + "\n")







#Main Function
def main():
    #Maximum delivery limit by the truck
    try:
        TruckNode.max_limit = int(inputFile.readline())
        #print("Max limit :", TruckNode.max_limit)

        #Root initialisation
        root = None

        #Reading the input file and populating the data to Binary Tree
        for i in inputFile.readlines():
            root = _readTruckRec(root, int(i))
    
        #Reading the prompt file and iterating through it
        for j in promptFile.read().splitlines():
            #print("j :", j)
            outputFile.write("------------- " + j + " --------------\n")
            P = j.split(": ")
            #print("P :", P)
            #print(root)

            if (P[0] == "printTruckRec"):
                outputFile.write("Total number of vehicles entered in the warehouse: " + str(TruckNode.numOfVariable) + "\n")
                _printTruckRec(root)

            elif (P[0] == "checkTruckRec"):
                _checkTruckRec(root, int(P[1]))

            elif(P[0] == "availTrucks"):
                _availTrucks(root)
                l = TruckNode.availTruckList
                outputFile.write( str(len(l)) + " Vehicle Ids that are currently available to deliver supplies:\n")
                for i in l:
                    outputFile.write(str(i)+"\n")

            elif(P[0] == "highFreqTrucks"):
                r = _highFreqTrucks(root, int(P[1]))
                if r is None:
                    outputFile.write("No such vehicle present in the system")
                else:
                    outputFile.write(r)

            elif (P[0] == "maxDeliveries"):
                outputFile.write("maxDeliveries: "+ str(TruckNode.max_limit) + "\n")
                _maxDeliveries(root)
                TruckNode.maxDeliveries.sort()
                outputFile.write( str(len(TruckNode.maxDeliveries)) + " Vehicle Ids did their maximum deliveries: \n")
                for i in TruckNode.maxDeliveries:
                    outputFile.write(str(i) + "\n")

            elif (P[0] == "updateTruckRec"):
                _updateTruckRec(root, int(P[1]))
                outputFile.write("Vehicle Id "+ P[1] +" record updated\n")

            elif (P[0] == "printOrderStatus"):
                outputFile.write("The following status of "+ P[1] + " orders:\n")
                _printOrderStatus(int(P[1]))

            outputFile.write("--------------------------------------\n")

        #Closing the files of input, output and prompt
        inputFile.close()
        outputFile.close()
        promptFile.close()

    #Exception handling if the File not found
    except FileNotFoundError:
        print("Could not read file: inputFile")
    #Exception handling if the File has invalid laterals/Charaters in the inputFile
    except ValueError:
        print("File is either empty or there could be invalid laterals in the inputFile")
    #Exceptions handling if some error occurred 
    except:
        print("Some Error Occurred!!!")
    
#setting the __name__ to main function
if __name__=="__main__":
    main()
