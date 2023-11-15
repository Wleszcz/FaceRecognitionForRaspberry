from guizero import App, Picture, PushButton
import cv2
from PIL import Image
import io

class ASWApp:
    app: App
    button: PushButton
    loaded_image = None

    def button_click(self):
        path = self.app.select_file()
        self.loaded_image = cv2.imread(path)

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.app = App("OpenCV and guizero Example")
        self.facecascade = cv2.CascadeClassifier("assets/haarcascade_frontalface_default.xml")
        self.init_gui()

    def init_gui(self):
        self.button = PushButton(self.app, self.app.select_file, text="Load Image")
        self.picture = Picture(self.app, image=None)

    def find_faces(self, frame):
        resized = cv2.resize(frame, (640, 480))
        grayFrame = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        faces = self.facecascade.detectMultiScale(grayFrame, 1.1, 4)
        return faces

    def update_gui(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = self.find_faces(frame)

        for x, y, w, h in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            if self.loaded_image:
                # cv2.image(frame, self.loaded_image, (x, y), (x + w, y + h))
                cv2.imshow(frame, self.loaded_image)

        img = Image.fromarray(frame)
        img = img.resize((640, 480))
        self.picture.image = img

    def run(self):
        self.app.repeat(70, self.update_gui)
        self.app.display()