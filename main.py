import sys
import FileLoad
import Ocr
import Search
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

file_obj = FileLoad.FileLoad()
ocr_obj = Ocr.Ocr()
data = file_obj.getData()
search_obj = Search.Search(data)

class MainWindow(QWidget):
    history = []

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # 左半分のレイアウト
        leftBox = QVBoxLayout()

        # テキスト検索
        self.textEdit = QLineEdit(self)
        self.textEdit.returnPressed.connect(self.wordClicked)
        leftBox.addWidget(self.textEdit)

        # 検索ボタン
        bbox = QHBoxLayout()
        ssButton = QPushButton('SS検索')
        ssButton.clicked.connect(self.ssClicked)
        bbox.addWidget(ssButton)
        wordButton = QPushButton('ワード検索')
        wordButton.clicked.connect(self.wordClicked)
        bbox.addWidget(wordButton)
        leftBox.addLayout(bbox)

        # 検索結果
        self.resultList = QListView(self)
        self.resultList.clicked.connect(self.resultClicked)
        self.resultList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.resultList.setAlternatingRowColors(True)
        self.resultList.setStyleSheet('alternate-background-color: #eee;background-color: #fff;')
        leftBox.addWidget(self.resultList)

        # 検索履歴
        self.historyList = QListView(self)
        self.historyList.clicked.connect(self.historyClicked)
        self.historyList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.historyList.setAlternatingRowColors(True)
        self.historyList.setStyleSheet('alternate-background-color: #eee;background-color: #fff;')
        leftBox.addWidget(self.historyList)

        # 右半分のレイアウト
        rigthBox = QVBoxLayout()

        # メインキャラコンボ
        self.charBox = QComboBox(self)
        model = QStringListModel()
        a = file_obj.getCharList()
        a.insert(0, '選択')
        model.setStringList(a)
        self.charBox.setModel(model)
        self.charBox.activated.connect(self.charActivated)
        rigthBox.addWidget(self.charBox)

        # メインキャラリスト
        self.charList = QListView(self)
        self.charList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.charList.setAlternatingRowColors(True)
        self.charList.setStyleSheet('alternate-background-color: #eee;background-color: #fff;')
        rigthBox.addWidget(self.charList)

        # レイアウト配置
        hbox = QHBoxLayout()
        hbox.addLayout(leftBox)
        hbox.addLayout(rigthBox)
        self.setLayout(hbox)

        self.setGeometry(0, 0, 800, 900)
        self.setWindowTitle('UmaChecker')

    def ssClicked(self):
        self.textEdit.text(ocr_obj.getString())
        self.view()

    def wordClicked(self):
        self.view()

    def resultClicked(self, item):
        self.history.insert(0, item.data())
        model = QStringListModel()
        model.setStringList(self.history)
        self.historyList.setModel(model)

    def historyClicked(self, item):
        del self.history[item.row()]
        model = QStringListModel()
        model.setStringList(self.history)
        self.historyList.setModel(model)

    def charActivated(self):
        a = file_obj.getCharData(self.charBox.currentText())
        model = QStringListModel()
        model.setStringList(a)
        self.charList.setModel(model)

    def view(self):
        word = search_obj.getWord(self.textEdit.text())
        res_list = []
        for i in word:
            str = '{}:{}\n'.format(i['e'], i['n'])
            for j in i['choices']:
                str += '{}:{}\n'.format(j['n'], j['t'].replace('[br]', ' '))
            res_list.append(str)
        model = QStringListModel()
        model.setStringList(res_list)
        self.resultList.setModel(model)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
