import os
import DataClass;
import GraphingUtil;

print "getting Paths..."
print ""

ProcessData = DataClass.ProcceserDataClass()

ProcessData.GetInputPath()
ProcessData.GetOutputPath()


print "Grabbing Data..."
print ""

Grabber = GraphingUtil.GraphDataGrabber()
GraphDatas = Grabber.Grabbit(ProcessData)

Grapher = GraphingUtil.GraphingUtil()
Grapher.Graphit(GraphDatas,ProcessData)