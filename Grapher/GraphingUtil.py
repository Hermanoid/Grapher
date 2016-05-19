import DataClass;
import matplotlib.pyplot as plt;
import csv
import os

class GraphingUtil:
    """A Utility that Graphs stuff."""
    def Graphit(self,GraphDatas,ProcessData):
        plt.figure()

class GraphDataGrabber:
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
                    if len(row)!=16:
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
            GraphDatas.append(GraphData)
        return GraphDatas





