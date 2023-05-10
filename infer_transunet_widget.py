# Copyright (C) 2021 Ikomia SAS
# Contact: https://www.ikomia.com
#
# This file is part of the IkomiaStudio software.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ikomia import utils, core, dataprocess
from infer_transunet.infer_transunet_process import TransunetParam
# PyQt GUI framework
from PyQt5.QtWidgets import *
from ikomia.utils.pyqtutils import BrowseFileWidget
from ikomia.utils import qtconversion


# --------------------
# - Class which implements widget associated with the process
# - Inherits PyCore.CProtocolTaskWidget from Ikomia API
# --------------------
class TransunetWidget(core.CWorkflowTaskWidget):

    def __init__(self, param, parent):
        core.CWorkflowTaskWidget.__init__(self, parent)

        if param is None:
            self.parameters = TransunetParam()
        else:
            self.parameters = param

        # Create layout : QGridLayout by default
        self.gridLayout = QGridLayout()

        self.qlabelConfigFile = QLabel("Select a config file (.yaml) :")
        self.qbrowseWidgetConfigFile = BrowseFileWidget(path=self.parameters.config_file, mode=QFileDialog.ExistingFile)

        self.qlabelModelFile = QLabel("Select a model file (.pth) :")
        self.qbrowseWidgetModelFile = BrowseFileWidget(path=self.parameters.model_path, mode=QFileDialog.ExistingFile)

        self.gridLayout.addWidget(self.qlabelConfigFile, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.qbrowseWidgetConfigFile, 0, 1, 1, 2)
        self.gridLayout.addWidget(self.qlabelModelFile, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.qbrowseWidgetModelFile, 1, 1, 1, 2)
        # PyQt -> Qt wrapping
        layout_ptr = qtconversion.PyQtToQt(self.gridLayout)

        # Set widget layout
        self.set_layout(layout_ptr)

    def on_apply(self):
        # Apply button clicked slot

        # Get parameters from widget
        self.parameters.config_file = self.qbrowseWidgetConfigFile.qedit_file.text()
        self.parameters.model_path = self.qbrowseWidgetModelFile.qedit_file.text()
        self.parameters.update = True

        # Send signal to launch the process
        self.emit_apply(self.parameters)


# --------------------
# - Factory class to build process widget object
# - Inherits PyDataProcess.CWidgetFactory from Ikomia API
# --------------------
class TransunetWidgetFactory(dataprocess.CWidgetFactory):

    def __init__(self):
        dataprocess.CWidgetFactory.__init__(self)
        # Set the name of the process -> it must be the same as the one declared in the process factory class
        self.name = "infer_transunet"

    def create(self, param):
        # Create widget object
        return TransunetWidget(param, None)
