
class ProceserDataClass(object):
	"""A Class storing Processing Data related to the Grapher Project"""
	def __init__(self):
		self.dsgt = []
class DataClass(object):
    def __init__(self):
        self.Timestamps = [];  self.Accel = {"X":[],"Y":[],"Z":[]}	
        self.Gyro = {"X":[],"Y":[],"Z":[]}
        self.Millis = []
        self.GForce = []
        self.GPSDat = {"lng":[],"lat":[],"Speed":[],"Altitude":[],"Accuracy":[],"Bearing":[]}

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

        if len(self.Accel["X"]) is not len(self.Accel["Y"]) or len(self.Accel["Z"]) is not len(self.Accel["X"]):
            raise ValueError("Accel axis are not the same length")                                           
        if len(self.Accel["X"]) is 0:
            raise ValueError("Accel Category is empty")


    def delAllStrs(self):
        """deletes strings from every sub catagory in the entire bank of data held in the DataClass instance
        
                self (an instance of DataClass)
            Returns:
                None
           """
        SectionList = [self.Timestamps, self.Gyro["X"], self.Gyro["Y"], self.Gyro["Z"], self.Millis,self.GForce, self.GPSDat["lng"], self.GPSDat["lat"], self.GPSDat["Speed"], 
                            self.GPSDat["Altitude"], self.GPSDat["Accuracy"], self.GPSDat["Bearing"]]
        for item in SectionList:
            print item
            self.delStrs(item) 

    def delStrs(self,item):
        """deletes all strings from LIST: string
            Parameters:
                item: list of values. 
            Returns:
                list of strings derived from 'item' with all strings removed."""
        for subItem in range(len(item)):
            try:
                if type(item[subItem]) == type("random string of glory"):
                    print item[subItem]
                    item.remove(item[subItem])
            except IndexError:
                break
        return item[:]
