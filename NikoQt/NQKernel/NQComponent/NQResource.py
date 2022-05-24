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

    def QImage(self, res_name):
        new_image = QImage()
        new_image.loadFromData(self.QByteArray(res_name))
        return new_image

    def QIcon(self, res_name):
        return QIcon(self.QPixmap(res_name))

    def QMovie(self, res_name):
        return QMovie(self.QBuffer(res_name))

    @staticmethod
    def get_size_of_media(media):
        try:
            return media.size()
        except:
            try:
                return media.scaledSize()
            except:
                return None

    @staticmethod
    def set_size_of_media(media, width, height):
        try:
            return media.scaled(QSize(width, height))
        except:
            try:
                return media.setScaledSize(QSize(width, height))
            except:
                return media

    @classmethod
    def scale(cls, media, px, stretch=False, compress=False):
        return cls.scale_by_width(
            cls.scale_by_height(media,
                                px,
                                stretch,
                                compress),
            px,
            stretch,
            compress)

    @classmethod
    def scale_by_width(cls, media, px, stretch=False, compress=False):
        if cls.get_size_of_media(media) is None:
            return media
        else:
            size = cls.get_size_of_media(media)
            real_width, real_height = size.width(), size.height()
            if stretch:
                if real_height < px:
                    real_width = int((real_width * px) / real_height)
                    real_height = px
            if compress:
                if real_height > px:
                    real_width = int((real_width * px) / real_height)
                    real_height = px

            return cls.set_size_of_media(media, real_width, real_height)

    @classmethod
    def scale_by_height(cls, media, px, stretch=False, compress=False):
        if cls.get_size_of_media(media) is None:
            return media
        else:
            size = cls.get_size_of_media(media)
            real_width, real_height = size.width(), size.height()
            if stretch:
                if real_width < px:
                    real_height = int((real_height * px) / real_width)
                    real_width = px
            if compress:
                if real_width > px:
                    real_height = int((real_height * px) / real_width)
                    real_width = px

            return cls.set_size_of_media(media, real_width, real_height)

    @classmethod
    def get_grayscale_image(cls, image):
        grayscale_image = image.convertToFormat(QImage.Format_Indexed8)
        grayscale_image.setColorCount(256)
        for i in range(256):
            grayscale_image.setColor(i, qRgb(i, i, i))
        return grayscale_image

    @classmethod
    def get_grayscale_pixmap(cls, pixmap):
        grayscale_image = cls.get_grayscale_image(pixmap.toImage())
        grayscale_pixmap = QPixmap().fromImage(grayscale_image)
        return grayscale_pixmap
