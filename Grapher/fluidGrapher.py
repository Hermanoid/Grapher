import GraphingUtil;
import DataClass;

templater = GraphingUtil.TemplateGrabber()
Template = templater.GetTemplate()
print Template
print Template.templateName
print Template.totalFiles
print Template.Files[Template.Files.keys()[0]].DatRows
print Template.ToInitString()