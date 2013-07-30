import os
import unittest
from __main__ import vtk, qt, ctk, slicer

#
# AnnotationsExporter
#

class AnnotationsExporter:
  def __init__(self, parent):
    parent.title = "Annotations Exporter"
    parent.categories = ["Utilities"]
    parent.dependencies = []
    parent.contributors = ["Felix Veysseyre (Kitware)"]
    parent.helpText = """
    To do.
    """
    parent.acknowledgementText = """
    This file was originally developed by Felix Veysseyre, Kitware Inc.
    """
    self.parent = parent

    # Add this test to the SelfTest module's list for discovery when the module
    # is created.  Since this module may be discovered before SelfTests itself,
    # create the list if it doesn't already exist.
    try:
      slicer.selfTests
    except AttributeError:
      slicer.selfTests = {}
    slicer.selfTests['AnnotationsExporter'] = self.runTest

  def runTest(self):
    tester = AnnotationsExporterTest()
    tester.runTest()

#
# qAnnotationsExporterWidget
#

class AnnotationsExporterWidget:
  def __init__(self, parent = None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()

  def setup(self):
    #
    # Load UI file
    #

    layoutFile = qt.QFile("/home/felix/Projects/AnnotationsExporter/AnnotationsExporter/Resources/UI/AnnotationsExporter.ui")
    layoutFile.open(qt.QFile.ReadOnly)
    self.landmarksExporterWidget = qt.QUiLoader().load(layoutFile)
    layoutFile.close()

    #
    # Get references
    #

    self.landmarksExporterWidget.setMRMLScene(slicer.mrmlScene)

    self.fiducialSelector = self.landmarksExporterWidget.findChild(slicer.qMRMLNodeComboBox, 'fiducialSelector')
    self.outputPath = self.landmarksExporterWidget.findChild(ctk.ctkPathLineEdit, 'outputPath')
    self.applyButton = self.landmarksExporterWidget.findChild(qt.QPushButton, 'applyButton')
    self.applyButton.connect('clicked()', self.onApplyButton)
    self.layout.addWidget(self.landmarksExporterWidget)

    #
    # Reload and Test area
    #

    reloadCollapsibleButton = ctk.ctkCollapsibleButton()
    reloadCollapsibleButton.text = "Reload and Test"
    self.layout.addWidget(reloadCollapsibleButton)
    reloadFormLayout = qt.QFormLayout(reloadCollapsibleButton)

    self.reloadButton = qt.QPushButton("Reload")
    self.reloadButton.toolTip = "Reload this module."
    self.reloadButton.name = "AnnotationsExporter Reload"
    reloadFormLayout.addWidget(self.reloadButton)
    self.reloadButton.connect('clicked()', self.onReload)

    self.reloadAndTestButton = qt.QPushButton("Reload and Test")
    self.reloadAndTestButton.toolTip = "Reload this module and then run the self tests."
    reloadFormLayout.addWidget(self.reloadAndTestButton)
    self.reloadAndTestButton.connect('clicked()', self.onReloadAndTest)

  def cleanup(self):
    pass

  def onApplyButton(self):
    fiducialList=self.fiducialSelector.currentNode()
    currentPath=self.outputPath.currentPath

    logic = AnnotationsExporterLogic()
    logic.run(fiducialList,currentPath)

  def onReload(self,moduleName="AnnotationsExporter"):
    """Generic reload method for any scripted module.
    ModuleWizard will subsitute correct default moduleName.
    """
    import imp, sys, os, slicer

    widgetName = moduleName + "Widget"

    # reload the source code
    # - set source file path
    # - load the module to the global space
    filePath = eval('slicer.modules.%s.path' % moduleName.lower())
    p = os.path.dirname(filePath)
    if not sys.path.__contains__(p):
      sys.path.insert(0,p)
    fp = open(filePath, "r")
    globals()[moduleName] = imp.load_module(
        moduleName, fp, filePath, ('.py', 'r', imp.PY_SOURCE))
    fp.close()

    # rebuild the widget
    # - find and hide the existing widget
    # - create a new widget in the existing parent
    parent = slicer.util.findChildren(name='%s Reload' % moduleName)[0].parent().parent()
    for child in parent.children():
      try:
        child.hide()
      except AttributeError:
        pass
    # Remove spacer items
    item = parent.layout().itemAt(0)
    while item:
      parent.layout().removeItem(item)
      item = parent.layout().itemAt(0)

    # delete the old widget instance
    if hasattr(globals()['slicer'].modules, widgetName):
      getattr(globals()['slicer'].modules, widgetName).cleanup()

    # create new widget inside existing parent
    globals()[widgetName.lower()] = eval(
        'globals()["%s"].%s(parent)' % (moduleName, widgetName))
    globals()[widgetName.lower()].setup()
    setattr(globals()['slicer'].modules, widgetName, globals()[widgetName.lower()])

  def onReloadAndTest(self,moduleName="AnnotationsExporter"):
    try:
      self.onReload()
      evalString = 'globals()["%s"].%sTest()' % (moduleName, moduleName)
      tester = eval(evalString)
      tester.runTest()
    except Exception, e:
      import traceback
      traceback.print_exc()
      qt.QMessageBox.warning(slicer.util.mainWindow(),"Reload and Test", 'Exception!\n\n' + str(e) + "\n\nSee Python Console for Stack Trace")

#
# AnnotationsExporterLogic
#

class AnnotationsExporterLogic:
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget
  """
  def __init__(self):
    pass

  def run(self,fiducialList,currentPath):
    """
    Run the actual algorithm
    """

    print("------------------------------------------------------------")
    print("-------------------- Annotations Exporter ------------------")
    print("------------------------------------------------------------")

    try:

      print("Fiducial list: " + fiducialList.GetName())

      if currentPath != "":

        print("Output file: " + currentPath)

        fichier = open(currentPath, "w")
        fiducials = vtk.vtkCollection()
        fiducialList.GetAllChildren(fiducials)

        print("------------------------------------------------------------")
        print("Working ...")

        for i in range(0,fiducials.GetNumberOfItems()):

          currentFiducial = fiducials.GetItemAsObject(i)

          if currentFiducial.GetClassName() == "vtkMRMLAnnotationFiducialNode":

            currentCoordinates = [0,0,0]
            currentFiducial.GetFiducialCoordinates(currentCoordinates)
            fichier.write(currentFiducial.GetName() + " : " + str(currentCoordinates[0]) + " " + str(currentCoordinates[1]) + " " + str(currentCoordinates[2]) + "\n")

        fichier.close()

        print("Done")

      else:

        print("Output file not valid")

    except Exception, e:

      print("Fiducial list not valid")

    print("------------------------------------------------------------")

    return True

class AnnotationsExporterTest(unittest.TestCase):
  """
  This is the test case for your scripted module.
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_AnnotationsExporter()

  def test_AnnotationsExporter(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests sould exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """
    pass
