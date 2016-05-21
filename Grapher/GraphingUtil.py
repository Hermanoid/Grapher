import DataClass
import matplotlib.pyplot as plt
import csv
import os

class GraphingUtil:
    """A Utility that Graphs stuff."""
    def Graphit(self,GraphDatas,ProcessData):
        ProcessData.outputDir = os.path.join(ProcessData.outputDir,self.getEmptyFileName(ProcessData.outputDir))
        os.mkdir(ProcessData.outputDir)
        for file in GraphDatas:
            print "{0}\r".format(self.FancyPercent(0,6)),
            fig,ax = plt.subplots(nrows=3,ncols=1)
            fig.set_size_inches(20.5,8.5)
            print "{0}\r".format(self.FancyPercent(1,6)),
            ax0 = ax[0].plot(file.Millis,file.Accel["X"],'r',file.Millis,file.Accel["Y"],'y',file.Millis,file.Accel["Z"],'g')
            ax[0].set_title("Accelerometer")
            ax[0].legend([ax0[0],ax0[1],ax0[2]],["X-axis","Y-axis","Z-axis"])
            ax[0].grid(True)
            print "{0}\r".format(self.FancyPercent(2,6)),
            ax1 =  ax[1].plot(file.Millis,file.AccelAvg,'b')
            ax[1].set_title("Accelerometer Average")
            ax[1].grid(True)
            ax[1].legend([ax1[0]],["All axis"])
            print "{0}\r".format(self.FancyPercent(3,6)),
            ax2 = ax[2].plot(file.Millis,file.Gyro["X"],'r',file.Millis,file.Gyro["Y"],'y',file.Millis,file.Gyro["Z"],'g')
            ax[2].set_title("Gyrometer")
            ax[2].grid(True)
            ax[2].legend([ax2[0],ax2[1],ax2[2]],["X-axis","Y-axis","Z-axis"])
            print "{0}\r".format(self.FancyPercent(4,6)),
            fig.savefig(os.path.join(ProcessData.outputDir,os.path.splitext(file.FileName)[0]+".png"), dpi = 80)
            print "{0}\r".format(self.FancyPercent(6,6)),
            print "{0}\r".format(""),
            print "{0}\r".format(file.FileName+" Saved!")
    def getEmptyFileName(self,path):
        listy = os.listdir(path)
        numTest = 1
        ItWorks = False
        while not ItWorks:
            if str(numTest) in listy:
                numTest=numTest+1
            else:
                ItWorks = True
        return str(numTest)
    def FancyPercent(self,completed,total):
        percent = float(completed)/float(total)*100
        return str(round(percent))+"%"
            

class GraphDataGrabber:
    """A utility that gets data from paths"""
    def Grabbit(self,ProcessData):
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
            GraphData.Millis =  GraphData.startAt0(GraphData.Millis)
            GraphDatas.append(GraphData)
        return GraphDatas





