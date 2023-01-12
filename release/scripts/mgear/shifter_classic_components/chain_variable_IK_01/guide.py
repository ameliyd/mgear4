from functools import partial

from mgear.shifter.component import guide
from mgear.core import pyqt
from mgear.vendor.Qt import QtWidgets, QtCore

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya.app.general.mayaMixin import MayaQDockWidget

from . import settingsUI as sui


# guide info
AUTHOR = "Miquel Campos"
URL = "www.mcsgear.com"
EMAIL = ""
VERSION = [1, 0, 0]
TYPE = "chain_variable_IK_01"
NAME = "chain"
DESCRIPTION = "Chain with variable number of IK controls"

##########################################################
# CLASS
##########################################################


class Guide(guide.ComponentGuide):
    """Component Guide Class"""

    compType = TYPE
    compName = NAME
    description = DESCRIPTION

    author = AUTHOR
    url = URL
    email = EMAIL
    version = VERSION

    def postInit(self):
        """Initialize the position for the guide"""

        self.save_transform = ["root", "#_loc"]
        self.save_blade = ["blade"]
        self.addMinMax("#_loc", 1, -1)

    def addObjects(self):
        """Add the Guide Root, blade and locators"""

        self.root = self.addRoot()
        self.locs = self.addLocMulti("#_loc", self.root)
        self.blade = self.addBlade("blade", self.root, self.locs[0])

        centers = [self.root]
        centers.extend(self.locs)
        self.dispcrv = self.addDispCurve("crv", centers)
        self.addDispCurve("crvRef", centers, 3)

    def addParameters(self):
        """Add the configurations settings"""

        self.pKeepLength = self.addParam("keepLength", "bool", False)
        self.pOverrideJointNb = self.addParam("overrideJntNb", "bool", False)
        self.pIkNb = self.addParam("ikNb", "long", 3, 1)
        self.pJntNb = self.addParam("jntNb", "long", 3, 1)
        self.pExtraTweak = self.addParam("extraTweak", "bool", False)

        self.pUseIndex = self.addParam("useIndex", "bool", False)
        self.pParentJointIndex = self.addParam(
            "parentJointIndex", "long", -1, None, None)

##########################################################
# Setting Page
##########################################################


class settingsTab(QtWidgets.QDialog, sui.Ui_Form):

    def __init__(self, parent=None):
        super(settingsTab, self).__init__(parent)
        self.setupUi(self)


class componentSettings(MayaQWidgetDockableMixin, guide.componentMainSettings):

    def __init__(self, parent=None):
        self.toolName = TYPE
        # Delete old instances of the componet settings window.
        pyqt.deleteInstances(self, MayaQDockWidget)

        super(self.__class__, self).__init__(parent=parent)
        self.settingsTab = settingsTab()

        self.setup_componentSettingWindow()
        self.create_componentControls()
        self.populate_componentControls()
        self.create_componentLayout()
        self.create_componentConnections()

    def setup_componentSettingWindow(self):
        self.mayaMainWindow = pyqt.maya_main_window()

        self.setObjectName(self.toolName)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle(TYPE)
        self.resize(280, 350)

    def create_componentControls(self):
        return

    def populate_componentControls(self):
        """Populate Controls

        Populate the controls values from the custom attributes of the
        component.

        """
        # populate tab
        self.tabs.insertTab(1, self.settingsTab, "Component Settings")

        # populate component settings
        self.populateCheck(self.settingsTab.keepLength_checkBox,
                           "keepLength")
        self.populateCheck(self.settingsTab.overrideJntNb_checkBox,
                           "overrideJntNb")
        self.populateCheck(self.settingsTab.extraTweak_checkBox,
                           "extraTweak")
        self.settingsTab.jntNb_spinBox.setValue(self.root.attr("jntNb").get())
        self.settingsTab.ikNb_spinBox.setValue(self.root.attr("ikNb").get())

    def create_componentLayout(self):

        self.settings_layout = QtWidgets.QVBoxLayout()
        self.settings_layout.addWidget(self.tabs)
        self.settings_layout.addWidget(self.close_button)

        self.setLayout(self.settings_layout)

    def create_componentConnections(self):

        self.settingsTab.keepLength_checkBox.stateChanged.connect(
            partial(self.updateCheck,
                    self.settingsTab.keepLength_checkBox,
                    "keepLength"))

        self.settingsTab.overrideJntNb_checkBox.stateChanged.connect(
            partial(self.updateCheck,
                    self.settingsTab.overrideJntNb_checkBox,
                    "overrideJntNb"))

        self.settingsTab.jntNb_spinBox.valueChanged.connect(
            partial(self.updateSpinBox,
                    self.settingsTab.jntNb_spinBox,
                    "jntNb"))

        self.settingsTab.ikNb_spinBox.valueChanged.connect(
            partial(self.updateSpinBox,
                    self.settingsTab.ikNb_spinBox,
                    "ikNb"))

        self.settingsTab.extraTweak_checkBox.stateChanged.connect(
            partial(self.updateCheck,
                    self.settingsTab.extraTweak_checkBox,
                    "extraTweak"))

    def dockCloseEventTriggered(self):
        pyqt.deleteInstances(self, MayaQDockWidget)
