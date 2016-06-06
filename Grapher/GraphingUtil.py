"""A Utility Module with Classes to assist in the gathering if data for and creation of Graphs"""

import DataClass
import matplotlib.pyplot as plt
import csv
import os
import numpy as np
import math
import datetime
class GraphingUtil:
    """A Utility that Graphs stuff."""
    def Graphit(self,GraphDatas,ProcessData):
        """A less-than-universal Graph Maker that creates a graph based on locations in ProcessData and data from the GraphDatas.
            Parameters:
                GraphDatas:
                    A list of DataClass objects with Accelerometer, AccelAvg, Gyrometer, FileName, and Milliseconds filled.
                ProcessData:
                    A ProcessData Object with outputDir completed
                Note:  GraphData objects can be created and filled by GraphingUtil.GraphDataGrabber.Grabbit(self,ProcessData)
                Note:  ProcessData Objects have built in functions allowing them to fill themselves (see ProcessData library)
            Returns:
                None.  Graphs are automatically named and saved to ProcessData.OutputDir """
        ProcessData.outputDir = os.path.join(ProcessData.outputDir,self.getEmptyFileName(ProcessData.outputDir))
        os.mkdir(ProcessData.outputDir)
        for file in GraphDatas:
            step = int(file.Millis[-1]/60)
            if step==0:
                step = 1
            xticks = range(0,int(file.Millis[-1]),step)
            print "{0}\r".format(self.FancyPercent(0,6)),
            fig,ax = plt.subplots(nrows=3,ncols=1)
            fig.set_size_inches(20.5,8.5)
            fig.suptitle(file.FileName)
            print "{0}\r".format(self.FancyPercent(1,6)),
            ax0 = ax[0].plot(file.Millis,file.Accel["X"],'r',file.Millis,file.Accel["Y"],'y',file.Millis,file.Accel["Z"],'g')
            ax[0].set_title("Accelerometer")
            ax[0].legend([ax0[0],ax0[1],ax0[2]],["X-axis","Y-axis","Z-axis"])
            ax[0].grid(True)
            ax[0].set_xticks(xticks)
            print "{0}\r".format(self.FancyPercent(2,6)),
            ax1 = ax[1].plot(file.Millis,file.AccelAvg,'b',file.Millis,file.GPSDat["Speed"],'m-')
            ax[1].set_title("Accelerometer Average/Speed")
            ax[1].grid(True)
            ax[1].legend([ax1[0],ax1[1]],["Accel AVG","Speed"])
            ax[1].set_xticks(xticks)
            print "{0}\r".format(self.FancyPercent(3,6)),
            ax2 = ax[2].plot(file.Millis,file.Gyro["X"],'r',file.Millis,file.Gyro["Y"],'y',file.Millis,file.Gyro["Z"],'g')
            ax[2].set_title("Gyrometer")
            ax[2].grid(True)
            ax[2].legend([ax2[0],ax2[1],ax2[2]],["X-axis","Y-axis","Z-axis"])
            ax[2].set_xticks(xticks)
            print "{0}\r".format(self.FancyPercent(4,6)),
            fig.savefig(os.path.join(ProcessData.outputDir,os.path.splitext(file.FileName)[0] + ".png"), dpi = 80)
            print "{0}\r".format(self.FancyPercent(6,6)),
            print "{0}\r".format(""),
            print "{0}\r".format(file.FileName + " Saved!")
    def getEmptyFileName(self,path):
        """Gets an empty, unused filenumber in the given path.  If folders 1-5 already exist in the directory, 6 will be returned
            Parameters:
                path (string):
                    An existing path.  Folders with numbers for names will be taken into effect on processing.
            Returns:
                filenumber (string):
                    The smallest possible filenumber (not negative) that is unused in the givenpath.
            Notes:
                This returns the smallest possible number, period.  If a given path has filenumbers 1,2, and 15, 3 will be still be returned, despite the 15. """
        listy = os.listdir(path)
        numTest = 1
        ItWorks = False
        while not ItWorks:
            if str(numTest) in listy:
                numTest = numTest + 1
            else:
                ItWorks = True
        return str(numTest)
    def FancyPercent(self,completed,total):
        """A simple utility to get percents to completion.
            Parameters:
                completed:
                    The number of steps (out of total) that have been completed.
                total:
                    The total number of steps.  If completed is equal to this,  percentage returned will be 100.00%.
            Returns:
                Percentage (string):  a percentage (derived from completed/total) that is accurate to the nearest hundredth and ends with a %."""
        percent = float(completed) / float(total) * 100
        return str(round(percent)) + "%"
    def getSpikes(self,data,minval=10,minIncrease=1.5):
        """A Utility that grabs the value of and locations of spikes in a list of data.
            Parameters:
                data:  
                    List of floats.
                minval:
                    the minimum value a data point has to be to be a spike.
                minIncrease:
                    the minimum amount a data point has to increase from the previous data point to be considered a spike
            Returns:
                tuple (SpikeVals (list), SpikeLocs (list):
                    SpikeVals:
                        The data points in the list that have been deemed spikes in data.
                    SpikeLocs:
                        The indexes in 'data' where a spike was found.
                """
        lastval = 0
        SpikeVals = []
        SpikeLocs = []
        for item in range(len(data)):
            if item == len(data):
                break
            if math.fabs(data[item]) >= minval:
                if (math.fabs(data[item]) - math.fabs(lastval)) >= minIncrease:
                    if data[item + 1] < data[item]:
                        SpikeVals.append(data[item])
                        SpikeLocs.append(item)
        lastval = data[item]
        return (SpikeVals,SpikeLocs)
    def SKGraphit(self,GraphDatas,ProcessData):
        ProcessData.outputDir = os.path.join(ProcessData.outputDir,self.getEmptyFileName(ProcessData.outputDir))
        os.mkdir(ProcessData.outputDir)
        for GraphData in GraphDatas:
            fig,ax = plt.subplots(nrows = len(GraphData.Dats),ncols=1)
            if len(GraphData.Dats) is 1:
                ax = [ax]
            
            TimeLength = GraphData.getGenericDataFor(GraphData.Dats[0]).get_Millis()[-1]
            if TimeLength<=60:
                fig.set_size_inches(20.5,8.5)
            else:
                fig.set_size_inches(20.5*(TimeLength/60),8.5)
            fig.suptitle(GraphData.FileName)
            Millis = GraphData.getGenericDataFor(GraphData.getShortestDat()).Millis
            for datIn in range(len(GraphData.Dats)):
                print "{0}\r".format(self.FancyPercent(datIn,len(GraphData.Dats) + 2)),
                Dat = GraphData.getGenericDataFor(GraphData.Dats[datIn])
                lines = ax[datIn].plot(Dat.get_Millis(),Dat.get_X(),'r-',Dat.get_Millis(),Dat.get_Y(),'g-',Dat.get_Millis(),Dat.get_Z(),'y-')
                ax[datIn].set_title(self.getFullName(GraphData.Dats[datIn]))
                ax[datIn].grid(True)
                if round(Dat.get_Millis()[-1])<=60:
                    ax[datIn].set_xticks(range(int(round(float(Dat.get_Millis()[-1])))))
                elif round(Dat.get_Millis()[-1])<=120:
                    ax[datIn].set_xticks(range(0,int(round(float(Dat.get_Millis()[-1]))),2))
                top = GraphData.Dats[datIn].split('.')[0]
                ax[datIn].legend([lines[0],lines[1],lines[2]],[top + "-X",top + "-Y",top + "-Z"])
            fig.savefig(os.path.join(ProcessData.outputDir,os.path.splitext(GraphData.FileName)[0] + ".png"), dpi = 160)
            print "{0}\r".format(GraphData.FileName + " Saved!")
    def getFullName(self,abbr):
        if abbr in ['acc.csv','acc','Acc','ACC','Accel','ACCEL','Accelerometer']:
            return "Accelerometer"
        if abbr in ['gyr.csv','gyr','Gyr','Gyro','GYR','GYRO','Gyrometer']:
            return "Gyrometer"
        if abbr in ['mag.csv','Mag','mag','MAG','Magnetometer']:
            return "Magnetometer"
        if abbr in ['rot.csv','rot','Rot','ROT','Rotation']:
            return "Rotation"
        
                
                
                
            

class GraphDataGrabber:
    """A utility that gets data from paths"""
    def Grabbit(self,ProcessData):
        """Grabs data from paths defined in ProcessData and returns a list of DataClass objects.
            Parameters:
                ProcessData:
                    a DataClass.ProcessData object with all data points filled.
            Returns:
                GraphDatas (list):
                    A list of DataClass.DataClass() objects with all data filled (accept TimeStamps, which are currently deleted)
            Note:  This Utility requires very specific data formats:
                FILES MUST BE .csv!
                Data Must be 16 rows in length or the entire row will be removed.
                Data must be convertable to float or it will be removed.
                Columns must be ordered as follows:
                    Timestamp,Accelerometer x-axis,Accelerometer y-axis,Accelermoter z-axis,Gyroscope x-axis,Gyroscope y-axis,Gyroscope z-axis,,Milliseconds Elapsed,G-Force,Longitude,Latitude,Speed,Altitude,Accuracy,Bearing"""
        GraphDatas = []
        for file in ProcessData.inputDirs:
            GraphData = DataClass.DataClass()
            print file
            if ProcessData.isFolder:
                reader = csv.reader(open(os.path.join(ProcessData.inputDir,file)))
            else:
                reader = csv.reader(open(os.path.join(os.path.dirname(ProcessData.inputDir),file)))
            GraphData.FileName = os.path.basename(file)
            for row in reader:
                try:
                    if len(row) != 8:
                        raise ValueError("bad length.  Catch this and cut this row out.")
                    GraphData.Timestamps.append(row[0])
                    GraphData.Accel["X"].append(row[1])
                    GraphData.Accel["Y"].append(row[2])
                    GraphData.Accel["Z"].append(row[3])
                    GraphData.Gyro["X"].append(row[4])
                    GraphData.Gyro["Y"].append(row[5])
                    GraphData.Gyro["Z"].append(row[6])
                    GraphData.GPSDat["Speed"].append(row[7])
                except IndexError:
                    Bob = "BOGUSNESS"
                except ValueError:
                    Bob = "still BOGUS!!!"
            GraphData.Millis = self.CreateMillisFromTimestamps(GraphData.Timestamps)
            GraphData.formatAllToFloat()
            GraphData.CreateAccAvg()
            GraphData.Millis.sort()
            GraphData.Millis = GraphData.startAt0(GraphData.Millis)
            GraphDatas.append(GraphData)
        return GraphDatas
    def SKGrabbit(self,ProcessData):
        GraphDatas = []
        runNames = []
        runDats = {}
        for file in ProcessData.inputDirs:
            if os.path.isfile(os.path.join(ProcessData.inputDir,file)) and '_' in file:
                split = file.split('_')
                if not split[0] in runNames:
                    runNames.append(split[0])
                    runDats[split[0]] = []
                runDats[split[0]].append(split[1])
        GraphDatas = []
        for run in runDats:
            print run
            GraphData = DataClass.DataClass()
            GraphData.FileName = run
            for dat in runDats[run]:
                reader = csv.reader(open(os.path.join(ProcessData.inputDir,run + '_' + dat)))
                GraphData.Dats.append(dat)
                for row in reader:
                    if dat == 'acc.csv':
                        GraphData.DDMillis.Accel.append(row[0])
                        GraphData.Accel["X"].append(row[1])
                        GraphData.Accel["Y"].append(row[2])
                        GraphData.Accel["Z"].append(row[3])
                    if dat == 'gyr.csv':
                        GraphData.DDMillis.Gyro.append(row[0])
                        GraphData.Gyro["X"].append(row[1])
                        GraphData.Gyro["Y"].append(row[2])
                        GraphData.Gyro["Z"].append(row[3])
                    if dat == 'mag.csv':
                        GraphData.DDMillis.Mag.append(row[0])
                        GraphData.Mag["X"].append(row[1])
                        GraphData.Mag["Y"].append(row[2])
                        GraphData.Mag["Z"].append(row[3])
                    if dat == 'rot.csv':
                        GraphData.DDMillis.Rot.append(row[0])
                        GraphData.Rot["X"].append(row[1])
                        GraphData.Rot["Y"].append(row[2])
                        GraphData.Rot["Z"].append(row[3])
            GraphData.formatAllToFloat()
            GraphDatas.append(GraphData)
        return GraphDatas
    def CreateMillisFromTimestamps(self,TimestampList):
        Timestamps = TimestampList[:]
        del Timestamps[0]
        format = "%H:%M:%S"
        TS0 = Timestamps[0]
        TSS = TS0.split(" ")
        TSS[1] = TSS[1][:-7]
        firstTime = datetime.datetime.strptime(TSS[1],format)
        tds = []
        for time in Timestamps:
            timeHalves = time.split(" ")
            timeHalves[1] = timeHalves[1][:-7]
            time = datetime.datetime.strptime(timeHalves[1],format)
            tds.append(time-firstTime)
        Secs = [td.seconds for td in tds]
        SecDict = {}
        for sec in Secs:
            if not str(sec) in SecDict:
                SecDict[str(sec)] = []
            SecDict[str(sec)].append(sec)
        DecedSecs = []
        SecDictKeys = sorted(SecDict.keys())
        for key in SecDictKeys:
            hertz = len(SecDict[key])
            interval = 1.0/float(hertz)
            for index in range(len(SecDict[key])):
                newItem = float(str(SecDict[key][index])+"."+str(int(index*index*100000)))
                DecedSecs.append(newItem)
                
        return DecedSecs
            
class TemplateGrabber():
    def GetTemplate(self):
        Presets = self.GetPresets()
        print "What template do you want to use?  Type 'Create' (Without Quotes) to create a new format, or use one of the following presets:"
        print Presets.keys()
        Template = raw_input(">>> ")
        if Template == "Create":
            return self.CreateTemplate()
        elif Template in Presets:
            return Presets[Template]
        else:
            return self.RetryGettingTemplate(Presets)
    def RetryGettingTemplate(self,Presets):
        print "That was not an existing Preset, or 'Create'.  Try again"
        Template = raw_input(">>> ")
        if Template == "Create":
            print self.CreateTemplate()
        elif Template in Presets:
            return Presets[Template]
        else:
            self.RetryGettingTemplate()
    def CreateTemplate(self):
        Template = DataClass.Template()
        def GetMultiFile():
            print "Is each Run spread out over multiple files? y/n"
            MultiFile = raw_input(">>> ")
            if MultiFile[0] is 'y':
                return True
            elif MultiFile[0] is 'n':
                return False
            else:
                print "That was not yes or no"
                GetMultiFile()
        def GetMultiDivider():
            MultiDivider = raw_input(">>> ")
            if len(MultiDivider) is 0:
                print "Please enter a character(s)"
                print "What character divides the filename and the Data Set?"
                GetMultiDivider()
            else:
                return MultiDivider
        def GetTotalFiles():
            TF = raw_input(">>> ")
            try:
                int(TF)
            except ValueError:
                print "That was not a number.  Try Again."
                GetTotalFiles()
            return int(TF)
        def GetNiceSuffix(num):
                SNLast = int(str(num)[-1])
                if SNLast == 1:
                    return "st"
                if SNLast == 2:
                    return "nd"
                if SNLast == 3:
                   return "rd"
                if SNLast in [0,4,5,6,7,8,9]:
                   return "th"
                else:
                    return "th"
        def MakeFileSetupFor(filenum):
            
            def getName():
                Name = raw_input(">>> ")
                if Name is "":
                    print "Please type something in."
                    return GetName()
                else:
                    return Name
            print "What is the suffix for the "+str(filenum)+GetNiceSuffix(filenum)+" file?"
            print "e.g. 'gyro' for ex_gyro.csv and 'accel' for ex_accel.csv"
            FileName = getName()
            return FileName,DataClass.Template.FileSetup()
        def GetTotalRows(filename):
            if filename is '__only__':
                print "how many rows are used in the data file?  This includes skipped rows."
            else:
                print "How many rows are used in "+filename+"?  This includes skipped rows."
            RowCount = raw_input(">>> ")
            if RowCount == "" or RowCount == "0":
                print "Please enter a value (other than 0)"
                GetTotalRows(filename)
            try:
                int(RowCount)
            except ValueError:
                print "That was not a number.  Keep in mind that decimals don't work."
                GetTotalRows(filename)
            return int(RowCount)
        def GetRowNameFor(filename,rownum):
            if filename == "__only__":
                print "What is the label for the "+str(rownum+1)+GetNiceSuffix(rownum+1)+" row in the data file?"
            else:
                print "What is the label for the "+str(rownum+1)+GetNiceSuffix(rownum+1)+" row in "+filename+"?"
            RowName = raw_input(">>> ")
            if RowName is "":
                print "please enter a value"
                return GetRowNameFor(filename,rownum)
            else:
                return RowName
        print '*'*80
        print ' '*19+"Welcome to the Super Template Maker 3000!!"
        print '*'*80
        print
        print "This program is designed to try to make things as simplified and easy to understand.  That means lots of words to read.  So, prepare to read."
        Template.isMultiFile = GetMultiFile()
        if Template.isMultiFile:
            print "What characters divides the filename and the Data Set?"
            print "(such as '_' for runName_gyro.csv"
            print "                        ^"
            Template.MultiFileDivider = GetMultiDivider()
            print "How many files will there be per run?"
            print "e.g. for files ex_gyro.csv, ex_accel.csv, and ex_Mag.csv, type '3'"
            print "               ^----1----^  ^-----2-----^     ^----3----^"
            Template.totalFiles = GetTotalFiles()
            for filenum in range(Template.totalFiles):
                filename,filesetup = MakeFileSetupFor(filenum)
                Template.Files[filename] = filesetup
        else:
            Template.Files['__only__'] = DataClass.Template.FileSetup()
            Template.totalFiles = 1
        for fileSetup in Template.Files:
            TFFS = Template.Files[fileSetup]
            TFFS.RowCount = GetTotalRows(fileSetup)
            print "Row names are fairly dynamic.  Separate Dats and SubDats with a dash."
            print "A Dat would be the gyro in 'gyro-x' and the subDat in 'gyro-x' would be 'X'"
            print "e.g. for gyro:  row 1 = gyro-X, row 2 = gyro-Y, row 3 = gyro-Z"
            print
            for row in range(TFFS.RowCount):
                TFFS.RowNames.append(GetRowNameFor(fileSetup,row))
            for rowName in TFFS.RowNames:
                if '-' in rowName:
                    Dat,SubDat = rowName.split('-')[:2]
                    if not Dat in TFFS.Dats:
                        TFFS.Dats.append(Dat)
                    if not Dat in TFFS.DatRows:
                        TFFS.DatRows[Dat] = {}
                    if not Dat in TFFS.SubDats:
                        TFFS.SubDats[Dat] = []
                    TFFS.SubDats[Dat].append(SubDat)
                    TFFS.DatRows[Dat][SubDat] = TFFS.RowNames.index(rowName)
                else:
                    TFFS.Dats.append(rowName)
                    TFFS.DatRows[rowName] = TFFS.RowNames.index(rowName)
        print "Last Step! Type the name of the template below.  It might pay to keep it brief, because this is what you'll type in every time you want to graph data with this template."
        Template.templateName = raw_input(">>> ")
        self.SaveTemplate(Template)
        return Template
    def GetPresets(self):
        Templates = {}
        try:
            PFile = open("Presets.txt")
            PString = PFile.readline()
            PFile.close()
            exec(PString)   
        except IOError:
            bob = "blobby"
        return Templates
    def SaveTemplate(self,Template):
        try:
            PFile = open("Presets.txt","r+")
        except IOError:
            PFile = open("Presets.txt","a")
            PFile.write("Templates = []")
            PFile.close()
            PFile = open("Presets.txt","r+")
        PFile.seek(-1,os.SEEK_END)
        PFile.truncate()
        PFile.seek(-1,os.SEEK_END)
        if not PFile.read(1) == '[':
            PFile.write(",")
        PFile.write(Template.ToInitString())
        PFile.write("]")
        PFile.close()
        
        
        
        
    
        
            

            





