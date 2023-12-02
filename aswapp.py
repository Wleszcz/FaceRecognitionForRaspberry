from guizero import App, Picture, PushButton, Text
import cv2
from PIL import Image, ImageDraw
from pyzbar.pyzbar import decode

alpha = 1.3  # Contrast control (1.0-3.0)
beta = 0  # Brightness control (0-100)

# python3 -m pip install pyzbar

class ASWApp:
    app: App
    code: Text
    loaded_image: Image = None
    bd = cv2.barcode.BarcodeDetector()
    last_code: str = ""

    def __init__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        self.app = App("OpenCV and guizero Example")
        self.facecascade = cv2.CascadeClassifier("assets/haarcascade_frontalface_default.xml")
        self.init_gui()

    def init_gui(self):
        self.code = Text(self.app, text="Shalom", size=20)
        self.picture = Picture(self.app, image=None)

    def update_gui(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

        # frame = cv2.imread("assets/Wiki-ean13.png")
        frame, s = self.getBarcode(frame)

        if s and s != self.last_code:
            print(s)
            self.last_code = s
            self.code.value = self.last_code
            #TODO PRINT TO LCD

        img = Image.fromarray(frame)

        img = img.resize((640, 480))
        self.picture.image = img

    def run(self):
        self.app.repeat(110, self.update_gui)
        self.app.display()

    def getBarcode(self, frame):
        s = ""
        for d in decode(frame):
            s = d.data.decode()
            frame = cv2.rectangle(frame, (d.rect.left, d.rect.top),
                                  (d.rect.left + d.rect.width, d.rect.top + d.rect.height), (0, 255, 0), 3)
            frame = cv2.putText(frame, s, (d.rect.left, d.rect.top + d.rect.height),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        return frame, s
