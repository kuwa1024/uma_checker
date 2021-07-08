import json

class FileLoad:
    data = []

    def __init__(self):
        # 選択肢データ読み込み
        json_open  = open('data.json', 'r', encoding='utf-8_sig')
        self.data = json.load(json_open)

    def getData(self):
        return self.data

    def getCharList(self):
        a = []
        for v in self.data:
            if v['c'] == 'c':
                a.append(v['n'])
        r = list(set(a))
        r.sort()
        return r

    def getCharData(self, name):
        res_list = []
        for i in self.data:
            if i['n'] == name:
                str = '{}:{}\n'.format(i['e'], i['n'])
                for j in i['choices']:
                    str += '{}:{}\n'.format(j['n'], j['t'].replace('[br]', ' '))
                res_list.append(str)
        return res_list
