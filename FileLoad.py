import json

class FileLoad:
    data = []

    def __init__(self):
        # 選択肢データ読み込み
        json_open  = open('data.json', 'r', encoding='utf-8_sig')
        self.data = json.load(json_open)

    def getData(self):
        return self.data
