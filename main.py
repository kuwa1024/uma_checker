import os, sys
import FileLoad
import Ocr
import Search
import japanize_kivy
from kivy.resources import resource_add_path, resource_find
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

Window.size = (400, 900)

file_obj = FileLoad.FileLoad()
ocr_obj = Ocr.Ocr()
data = file_obj.getData()
search_obj = Search.Search(data)

class MyLayout(BoxLayout):
    # プロパティの追加
    input = None
    label1 = None
    label2 = None
    label3 = None
    labelh = None
    tmp_text = ''

    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 40:
            self.wordClicked()

    def ssClicked(self):
        self.input.text = ocr_obj.getString()
        self.view()

    def wordClicked(self):
        self.view()

    def label1Clicked(self):
        self.tmp_text = self.label1.text
        self.labelClicked()

    def label2Clicked(self):
        self.tmp_text = self.label2.text
        self.labelClicked()

    def label3Clicked(self):
        self.tmp_text = self.label3.text
        self.labelClicked()

    def labelClicked(self):
        self.labelh.text = self.tmp_text + '\n' + self.labelh.text

    def view(self):
        word = search_obj.getWord(self.input.text)
        res_list = []
        for v in word:
            result = ''
            question = v[4].split()
            for i in range(len(question), 3):
                question.append('')
            answer = v[5].split()
            for i in range(len(answer), 3):
                answer.append('')
            result += v[1] + ' : ' + v[2] + ' : ' + v[0] + '\n'
            for i in range(0, len(question)):
                if answer[i]:
                    result += question[i] + ' : ' + answer[i] + '\n'
            res_list.append(result)
        for i in range(len(res_list), 3):
            res_list.append('')
        self.label1.text = res_list[0]
        self.label2.text = res_list[1]
        self.label3.text = res_list[2]

class UmaApp(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    UmaApp().run()
