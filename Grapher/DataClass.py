import os
class ProcceserDataClass(object):
    """A Class storing Processing Data related to the Grapher Project"""
    def __init__(self):
        self.inputDir = ""
        self.inputDirs = []
        self.isFolder = False
        self.outputDir = ""
    def GetOutputPath(self):
        self.outputDir = raw_input("What path should be outputted to?\n\r>>> ")
        if self.outputDir is "":
            self.outputDir = "C:\Users\Lucas\Pictures\GraphOutput"
        bob = os.path.isabs(self.inputDir)
        if not bob:
            print "that was not an excepted path name.  Try again"
            self.GetOutputPath()
    def GetInputPath(self):
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
    def __init__(self):
        self.Timestamps = []
        self.Accel = {"X":[],"Y":[],"Z":[]}	
        self.Gyro = {"X":[],"Y":[],"Z":[]}
        self.Millis = []
        self.GForce = []
        self.GPSDat = {"lng":[],"lat":[],"Speed":[],"Altitude":[],"Accuracy":[],"Bearing":[]}
        self.FileName = ""

    def Process(self):
        self.delAllStrs()

    def toList(self):
        """
            Returns a list of all the categories contained my DataClass.  Note that dictionaries such as GPSDat are returned in dictionary form.
        """
        return [self.Timestamps,self.Accel,self.Gyro,self.Millis,self.GForce,self.GForce,self.GPSDat]

    def CreateAccAvg(self):
        """
            Creates AVG category under the DataClass instance.  Note that this category does not return with toList() or any other to-things(), and does not get strings deleted with delAllStrs(), although that is not nessessary as no strings are created under it in the first place
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
        SectionList = [self.Accel["X"], self.Accel["Y"], self.Accel["Z"], self.Gyro["X"], self.Gyro["Y"], self.Gyro["Z"], self.Millis,self.GForce,
                       self.GPSDat["lng"], self.GPSDat["lat"], self.GPSDat["Speed"], self.GPSDat["Altitude"], self.GPSDat["Accuracy"], self.GPSDat["Bearing"]]
        for item in SectionList:
            del item[0]
        del self.Timestamps

        for item in SectionList:
            for SubItem in range(len(item)):
                item[SubItem] = float(item[SubItem])