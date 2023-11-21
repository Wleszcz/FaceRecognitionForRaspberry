from guizero import App, Picture, PushButton, Text
import cv2
from PIL import Image, ImageDraw
import io


class ASWApp:
    app: App
    button: PushButton
    count: Text
    loaded_image: Image = None

    def getfile(self):
        path = self.app.select_file()
        if path:
            self.loaded_image = Image.open(path)

    def __init__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        self.app = App("OpenCV and guizero Example")
        self.facecascade = cv2.CascadeClassifier("assets/haarcascade_frontalface_default.xml")
        self.init_gui()

    def init_gui(self):
        self.button = PushButton(self.app, command=self.getfile, text="Load Image")
        self.count = Text(self.app, text="Shalom", size=20)
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

        img = Image.fromarray(frame)
        img = self.draw_faces(img, self.find_faces(frame))

        img = img.resize((640, 480))
        self.picture.image = img

    def run(self):
        self.app.repeat(100, self.update_gui)
        self.app.display()

    def draw_faces(self, img, faces):
        self.count.value = "Faces detected: " + str(len(faces))
        for x, y, w, h in faces:
            if self.loaded_image:
                copy = self.loaded_image.copy()
                copy = copy.resize((w, h))
                img.paste(copy, (x, y), copy)

            img1 = ImageDraw.Draw(img)
            img1.rectangle(((x, y), (x + w, y + h)), outline="red")
        return img
