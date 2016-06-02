"""A Utility Module with Classes to assist in the gathering if data for and creation of Graphs"""

import DataClass
import matplotlib.pyplot as plt
import csv
import os
import numpy as np
import math
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
            file.MillisToSec()
            print "{0}\r".format(self.FancyPercent(0,6)),
            fig,ax = plt.subplots(nrows=3,ncols=1)
            fig.set_size_inches(20.5,8.5)
            fig.suptitle(file.FileName)
            print "{0}\r".format(self.FancyPercent(1,6)),
            ax0 = ax[0].plot(file.Millis,file.Accel["X"],'r',file.Millis,file.Accel["Y"],'y',file.Millis,file.Accel["Z"],'g')
            ax[0].set_title("Accelerometer")
            ax[0].legend([ax0[0],ax0[1],ax0[2]],["X-axis","Y-axis","Z-axis"])
            ax[0].grid(True)
            print "{0}\r".format(self.FancyPercent(2,6)),
            ax1 = ax[1].plot(file.Millis,file.AccelAvg,'b',file.Millis,file.GPSDat["Speed"],'m-')
            ax[1].set_title("Accelerometer Average/Speed")
            ax[1].grid(True)
            ax[1].legend([ax1[0],ax1[1]],["Accel AVG","Speed"])
            print "{0}\r".format(self.FancyPercent(3,6)),
            ax2 = ax[2].plot(file.Millis,file.Gyro["X"],'r',file.Millis,file.Gyro["Y"],'y',file.Millis,file.Gyro["Z"],'g')
            ax[2].set_title("Gyrometer")
            ax[2].grid(True)
            ax[2].legend([ax2[0],ax2[1],ax2[2]],["X-axis","Y-axis","Z-axis"])
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
                    if len(row) != 16:
                        raise ValueError("bad length.  Catch this and cut this row out.")
                    GraphData.Timestamps.append(row[0])
                    GraphData.Accel["X"].append(row[1])
                    GraphData.Accel["Y"].append(row[2])
                    GraphData.Accel["Z"].append(row[3])
                    GraphData.Gyro["X"].append(row[4])
                    GraphData.Gyro["Y"].append(row[5])
                    GraphData.Gyro["Z"].append(row[6])

                    GraphData.Millis.append(row[8])
                    GraphData.GForce.append(row[9])
                    GraphData.GPSDat["lng"].append(row[10])
                    GraphData.GPSDat["lat"].append(row[11])
                    GraphData.GPSDat["Speed"].append(row[12])
                    GraphData.GPSDat["Altitude"].append(row[13])
                    GraphData.GPSDat["Accuracy"].append(row[14])
                    GraphData.GPSDat["Bearing"].append(row[15])
                except IndexError:
                    Bob = "BOGUSNESS"
                except ValueError:
                    Bob = "still BOGUS!!!"
            GraphData.formatAllToFloat()
            GraphData.CreateAccAvg()
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


            





