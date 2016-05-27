"""A Storage module with Classes providing storage for Graph Data and basic data modification utilities."""
import os
class ProcceserDataClass(object):
    """A Class storing Processing Data related to the Grapher Project"""
    def __init__(self):
        self.inputDir = ""
        self.inputDirs = []
        self.isFolder = False
        self.outputDir = ""
    def GetOutputPath(self):
        """Gets an output path from the user with less-than-foolproof path checking.
            Parameters: 
                None
            Returns:
                None
            """
        self.outputDir = raw_input("What path should be outputted to?\n\r>>> ")
        if self.outputDir is "":
            self.outputDir = "C:\Users\Lucas\Pictures\GraphOutput"
        bob = os.path.isabs(self.inputDir)
        if not bob:
            print "that was not an excepted path name.  Try again"
            self.GetOutputPath()
    def GetInputPath(self):
        """Grabs an input path from the user with relatively foolproof path checking, and processes the inputed path
            Parameters:
                None
            Returns:
                None"""
        self.inputDir = raw_input("Where should files be read from?  This can be a file or a folder of files\n\r>>> ")
        if os.path.isabs(self.inputDir):
            if os.path.isdir(self.inputDir):
                self.isFolder = True
                self.inputDirs = os.listdir(self.inputDir)
            elif os.path.isfile(self.inputDir):
                self.isFolder = False
                self.inputDirs = [self.inputDir]
            else:
                print "That path does not exist.  Try again"
                self.GetInputPath()
        else:
            print "that was not an excepted path name.  Try again."
            self.GetInputPath()
class DataClass(object):
    """A storage utility providing storage and certain modification functions to movement data such as Gyroscope, Accelerometer, Milliseconds, Lat/long, etc."""
    def __init__(self):
        """Creates a DataClass instance with the following datasets initialized:
            TimeStamps:
                list
            Accel:
                Dictionary:
                    "X":list
                    "Y":list
                    "Z":list
            Gyro:
                Dictionary:
                    "X":list, "Y":list, "Z":list  
            Millis:
                list
            GForce:
                list
            GPSDat:
                Dictionary:
                    "lng":list
                    "lat":list
                    "Speed":list
                    "Altitude":list
                    "Accuracy":list
                    "Bearing":list
            FileName:
                String
"""
        self.Timestamps = []
        self.Accel = {"X":[],"Y":[],"Z":[]}	
        self.Gyro = {"X":[],"Y":[],"Z":[]}
        self.Mag = {"X":[],"Y":[],"Z":[]}
        self.Rot = {"X":[],"Y":[],"Z":[]}
        self.Millis = []
        self.GForce = []
        self.GPSDat = {"lng":[],"lat":[],"Speed":[],"Altitude":[],"Accuracy":[],"Bearing":[]}
        self.FileName = ""
        self.Dats = []
    def avgAllTo(self,RPS):
        raise NotImplementedError()
        SectionList = [self.Accel["X"], self.Accel["Y"], self.Accel["Z"], self.Gyro["X"], self.Gyro["Y"], self.Gyro["Z"], self.Millis,self.GForce,
                       self.GPSDat["lng"], self.GPSDat["lat"], self.GPSDat["Speed"], self.GPSDat["Altitude"], self.GPSDat["Accuracy"], self.GPSDat["Bearing"]]
        
        for section in SectionList:
            self.avgTo(section,RPS)
    def avgTo(self,item,RPS):
        raise NotImplementedError()
        sectLen = 1.0 / RPS
        sects = {}
        sect = 1
        print item
        for val in item:
            valExcepted = False
            while not valExcepted:
                if float(val) < float(sect * sectLen):
                    try:
                        sects[str(sect)].append(val)
                    except KeyError:
                        sects[str(sect)] = []
                        sects[str(sect)].append(val)
                    valExcepted = True
                else:
                    sect = sect + 1
        return sects    
    def SyncTo(self,itemMillis,targetedMillis,item):
        if not len(itemMillis) == len(item):
            raise ValueError("Item and ItemMillis must have same length")
        newSet = {}
        on = 0
        for time in targetedMillis:
            newSet[str(time)] = []
            GoOn = True
            while GoOn:
                if round(itemMillis[on],ndigits=2)==round(time,ndigits=2):
                    newSet[str(time)].append(item[on])
                    on = on+1
                else:
                    GoOn=False
        for time in newSet:
            if newSet[time]:
                There = False
                while not There:
                    
                    
    def startAt0(self,List):
        """starts the first value of 'list' at zero, and counts all other values up from there.
        Parameters:
            List: a list with multiple ints or floats
        Returns:
            A list derived from 'List' that starts at 0
        """
        cutOff = List[0]
        
        for item in range(len(List)):
            List[item] = List[item] - cutOff
        return List
    def getGenericDataFor(self,datName):
        if datName in ['acc.csv','acc','Acc','ACC','Accel','ACCEL','Accelerometer']:
            return GenericDat(self.Accel["X"],self.Accel["Y"],self.Accel["Z"])
        if datName in ['gyr.csv','gyr','Gyr','Gyro','GYR','GYRO','Gyrometer']:
            return GenericDat(self.Gyro["X"],self.Gyro["Y"],self.Gyro["Z"])
        if datName in ['mag.csv','Mag','mag','MAG','Magnometer']:
            return GenericDat(self.Mag["X"],self.Mag["Y"],self.Mag["Z"])
        if datName in ['rot.csv','rot','Rot','ROT','Rotation']:
            return GenericDat(self.Rot["X"],self.Rot["Y"],self.Rot["Z"])
    def MillisToSec(self):
        """A simple, convenient Utlity that converts the Milliseconds section of a DataClass instance to seconds
            Parameters:
                None
            Returns:
                the DataClass.Millis section
            Note:
                This function does not rename the section, so be careful and remember that the data under DataClass.Millis is actually in seconds after using this."""
        self.Millis = [item / 1000 for item in self.Millis]
        return self.Millis
    def CreateAccAvg(self):
        """Creates AVG category under the DataClass instance.  Note that this category does not return with toList() or any other to-things(), and does not get strings deleted with delAllStrs(), although that is not nessessary as no strings are created under it in the first place
         Parameters:  
            self (DataClass instance)
        Requires:
            DataClass instance has data under  Accel on all axis, and all axis are the same length
        Returns:
             None
         """
                                      
        if len(self.Accel["X"]) is 0:
            raise ValueError("Accel Category is empty")
        self.AccelAvg = []

        for item in range(len(self.Accel["X"])):
            for axis in ["X","Y","Z"]:
                if type(self.Accel[axis][item]) != type(123.345):
                    raise ValueError("non-number included in Accel bank.  Use formatAllToFloat() to remove strings.")
            self.AccelAvg.append((self.Accel["X"][item] + self.Accel["Y"][item] + self.Accel["Z"][item]) / 3)
    def formatAllToFloat(self):
        """deletes strings from every sub catagory in the entire bank of data held in the DataClass instance
        
                self (an instance of DataClass)
            Returns:
                None
           """
        SectionList = [self.Accel["X"], self.Accel["Y"], self.Accel["Z"], self.Gyro["X"], self.Gyro["Y"], self.Gyro["Z"], self.Millis,self.GForce,self.Rot["X"],self.Rot["Y"],self.Rot["Z"],
                       self.GPSDat["lng"], self.GPSDat["lat"], self.GPSDat["Speed"], self.GPSDat["Altitude"], self.GPSDat["Accuracy"], self.GPSDat["Bearing"],self.Mag["X"],self.Mag["Y"],self.Mag["Z"]]

        for item in SectionList:
            if not len(item) == 0:
                for SubItem in range(len(item)):
                    try:
                        if SubItem > len(item):
                            break
                        else:
                            item[SubItem] = float(item[SubItem])
                    except ValueError:
                        try:
                            del item[SubItem]
                        except IndexError:
                            "Slightly dangerous catch...."
                    except IndexError:
                        "yo"

class GenericDat(object):
    def __init__(self):
        self.Dat = {"X":[],"Y":[],"Z":[]}
    def __init__(self,X,Y,Z):
        self.Dat = {"X":X,"Y":Y,"Z":Z}
    def set_X(self,list):
        self.Dat["X"] = list
    def set_Y(self,list):
        self.Dat["Y"] = list
    def set_Z(self,list):
        self.Dat["Z"] = list
    def get_X(self):
        return self.Dat["X"]
    def get_Y(self):
        return self.Dat["Y"]
    def get_Z(self):
        return self.Dat["Z"]
    def set(self,Key,list):
        self.Dat[Key] = list
    def get(self,Key):
        return self.Dat[Key]