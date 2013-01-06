import loaders


class ebase(object):
    def __init__(self):
        pass

    def load_data(self,data):
        self.img = loaders.load_img(data['img'])
        self.lang = loaders.load_lang(data['lang_file.json'])
