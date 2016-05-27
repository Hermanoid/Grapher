import GraphingUtil
import DataClass

ProcessData = DataClass.ProcceserDataClass()

ProcessData.GetInputPath()
ProcessData.GetOutputPath()

Grabber = GraphingUtil.GraphDataGrabber()

GraphDatas = Grabber.SKGrabbit(ProcessData)

Grapher = GraphingUtil.GraphingUtil()

Grapher.SKGraphit(GraphDatas,ProcessData)