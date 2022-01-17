from NikoKit.NikoLib.NKResource import NKResource
from NikoKit.NikoQt.NQAdapter import *


class NQResource(NKResource):
    def QByteArray(self, res_name):
        return QByteArray.fromBase64(self.res[res_name])

    def QBuffer(self, res_name):
        return QBuffer().setData(self.QByteArray(res_name))

    def QPixmap(self, res_name):
        new_pixmap = QPixmap()
        new_pixmap.loadFromData(self.QByteArray(res_name))
        return new_pixmap

    def QIcon(self, res_name):
        return QIcon(self.QPixmap(res_name))

    def QMovie(self, res_name):
        return QMovie(self.QBuffer(res_name))
