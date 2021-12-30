import pyimgur

CLIENT_ID = "5cf66fc9dcfb7a0"


class ImgSender:
    def __init__(self, path):
        self.PATH = path

    def send(self):
        im = pyimgur.Imgur(CLIENT_ID)
        uploaded_image = im.upload_image(self.PATH)
        # print(uploaded_image.title)
        return uploaded_image.link
