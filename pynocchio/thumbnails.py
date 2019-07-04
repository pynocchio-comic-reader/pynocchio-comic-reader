from PyQt5 import QtCore, QtGui, QtWidgets

from .comic_page_handler_factory import ComicPageHandlerFactory
from .uic_files import thumbnails_ui


class ThumbnailsDock(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.ui = thumbnails_ui.Ui_Thumbnails()
        self.ui.setupUi(self)

        self.thumb_size = QtCore.QSize(100, 100)

        color = self.palette().highlight().color()
        self.hl = 'background-color:rgba({},{},{},150);'.format(color.red(),color.green(),color.blue())

        self.thumbs = []
        self.page = None

    def clear(self):

        while self.ui.verticalLayout.count() > 0:
            item = self.ui.verticalLayout.takeAt(0)
            if not item:
                continue
            w = item.widget()
            if w:
                w.setParent(None)

        self.thumbs = []
        self.page = None

        QtGui.QGuiApplication.processEvents()

    def populate(self, current=None):
        pages = self.parent().model.comic_page_handler.comic.pages
        self.ui.widget.adjustSize()

        for i, p in enumerate(pages):
            pix_map = QtGui.QPixmap()
            pix_map.loadFromData(p.data)
            pix_map = pix_map.scaled(self.thumb_size,
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation)
            w = self.thumb_widget(pix_map, i)
            self.thumbs.append(w)
            self.ui.verticalLayout.addWidget(w)
            if (i == current):
                self.highlight(i)
            QtGui.QGuiApplication.processEvents()

        self.ui.widget.adjustSize()

    def thumb_widget(self, pix_map, num):
        w = QtWidgets.QWidget()
        l = QtWidgets.QVBoxLayout()
        b = QtWidgets.QPushButton()
        b.setFlat(True)
        b.setIcon(QtGui.QIcon(pix_map))
        b.setIconSize(pix_map.size())
        b.adjustSize()
        b.clicked.connect(lambda state, i=num: self.go_to_page(i))
        n = QtWidgets.QLabel(str(num+1))
        l.addWidget(b, 0, QtCore.Qt.AlignHCenter)
        l.addWidget(n, 0, QtCore.Qt.AlignHCenter)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(0)
        w.setLayout(l)
        w.setObjectName('thumb_{}'.format(num))
        return w

    def go_to_page(self, num):
        self.parent()._go_to_page(num)

    def highlight(self, num):
        try:
            self.thumbs[self.page].setStyleSheet('')
        except (TypeError, IndexError):
            pass
        try:
            self.thumbs[num].setStyleSheet('#thumb_{}{{{}}}'.format(num, self.hl))
            self.ui.dockWidgetContents.ensureWidgetVisible(self.thumbs[num])
            self.page = num
        except (TypeError, IndexError):
            pass
