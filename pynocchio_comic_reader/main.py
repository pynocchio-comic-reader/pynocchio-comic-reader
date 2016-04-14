# coding=UTF-8
#
# Copyright (C) 2015  Michell Stuttgart

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.

# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
from PySide import QtGui, QtCore

import lib.main_window_model
import lib.main_window_view


class App(QtGui.QApplication):

    def __init__(self, sys_argv):
        QtGui.QApplication.__init__(self, sys_argv)

        self.setApplicationName('Pynocchio Comic Reader')
        self.setApplicationVersion('1.0.9')

        qm = QtCore.QLocale.system().name()

        if qm != 'en_US':
            translator = QtCore.QTranslator()
            try:
                translator.load('locale/qt_%s.qm' % qm)
                self.installTranslator(translator)
            except IOError:
                print 'Translation file qt_%s.qm not find' % qm

        self.model = lib.main_window_view.MainWindowModel()
        self.view_control = lib.main_window_view.MainWindowView(self.model)
        self.view_control.show()

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
