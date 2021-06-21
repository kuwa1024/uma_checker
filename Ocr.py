import os
import pyocr
from PIL import Image
from pywinauto import application

class Ocr:
    tool = []

    def __init__(self):
        # Tesseractのパスを通す
        path_tesseract = 'C:\\Program Files\\Tesseract-OCR'
        if path_tesseract not in os.environ['PATH'].split(os.pathsep):
            os.environ['PATH'] += os.pathsep + path_tesseract

        # OCRエンジンの取得
        tools = pyocr.get_available_tools()
        self.tool = tools[0]

    def getString(self):
        # スクリーンショット
        app = application.Application().connect(title='umamusume')
        app[u'umamusume'].capture_as_image().save('umamusume.png')

        # 選択肢抜き出し
        im = Image.open('umamusume.png')
        w, h = im.size
        im_crop = im.crop((w*0.12, h*0.55, w*0.8, h*0.59))
        im_crop.save('umamusume_one.jpg', quality=100)

        img_org = Image.open('umamusume_one.jpg')
        builder = pyocr.builders.TextBuilder()
        result = self.tool.image_to_string(img_org, lang='jpn', builder=builder)
        return result[:-1].replace('ぞ', ' ').replace('ど', ' ').replace('ぐ', ' ')
