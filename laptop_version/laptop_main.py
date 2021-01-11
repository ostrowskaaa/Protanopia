from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.uix.effectwidget import EffectWidget, EffectBase
from kivy.clock import Clock

import time

from PIL import Image as Im
import numpy as np
import cv2

Builder.load_file('editor.kv')


class MenuScreen(Screen):
    pass


class CameraWidget(Image):
    def __init__(self, **kwargs):
        super(CameraWidget, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0/33.0)
        Fra = None

    def update(self, dt):
        ret, frame = self.capture.read()
        buf1 = frame
        self.Fra = buf1
        r_new = np.uint8(protanopia_filter(0.56667, 0.43333, 0, buf1))
        g_new = np.uint8(protanopia_filter(0.55833, 0.44167, 0, buf1))
        b_new = np.uint8(protanopia_filter(0, 0.24167, 0.75833, buf1))
        rgb = np.dstack((r_new, g_new, b_new))
        buf = rgb.tostring()

        texture1 = Texture.create(size=(frame.shape[1],
                                        frame.shape[0]), colorfmt='rgb')
        texture1.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.texture = texture1


class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        self.camera = CameraWidget()
        self.add_widget(self.camera)


class UploadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Upload(Screen):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def show_load_list(self):
        content = UploadDialog(load=self.load_list, cancel=self.dismiss_popup)
        self._popup = Popup(title='Choose photo to upload',
                            content=content,
                            size_hint=(1, 1))
        self._popup.open()

    def load_list(self, path):
        try:
            filename = ('.').join(path[0].split('.')[:-1])
            img = Im.open(path[0])
            r_new = np.uint8(protanopia_filter(0.56667, 0.43333, 0, img))
            g_new = np.uint8(protanopia_filter(0.55833, 0.44167, 0, img))
            b_new = np.uint8(protanopia_filter(0, 0.24167, 0.75833, img))
            rgb = np.dstack((r_new, g_new, b_new))
            new_img = Im.fromarray(rgb, 'RGB')
            new_img.save(str(filename) + '_new.jpg')
            self.ids.image.source = str(filename) + '_new.jpg'
        except:
            pass

    def dismiss_popup(self):
        self._popup.dismiss()


class About(Screen):
    pass


class ProtanopiaWorld(App):
    def build(self):
        self.icon = 'data/logo.png'
        self.title = 'Colorblindness'
        return sm


def protanopia_filter(R, G, B, img):
    arr = np.array(img)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    new_color = []
    for i in range(len(r)):
        Rr, Gg, Bb = R * r[i], G * g[i], B * b[i]
        value = Rr + Gg + Bb
        new_color.append(value)
    return new_color


sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(CameraScreen(name='camera'))
sm.add_widget(Upload(name='upload'))
sm.add_widget(About(name='about'))

if __name__ == '__main__':
    ProtanopiaWorld().run()
