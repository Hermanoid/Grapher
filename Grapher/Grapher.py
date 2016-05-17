import os
import DataClass;
import GraphingUtil;

print "getting Paths..."
print ""

ProcessData = DataClass.ProcesserDataClass()

ProcessData.GetInputPath()
ProcessData.GetOutputPath()
ProcessData.ProcessPaths()


print "Grabbing Data..."
print ""

Grabber = GraphingUtil.GraphDataGrabber()
GraphDatas = Grabber.Grabbit(ProcessData)
print GraphDatas

Grapher = GraphingUtil.GraphingUtil()