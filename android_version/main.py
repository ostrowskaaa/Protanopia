from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

import time

from PIL import Image
import numpy as np

from android.permissions import request_permissions, Permission
request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

Builder.load_file('editor.kv')

class MenuScreen(Screen):
    pass

class UploadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Upload(Screen):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def show_load_list(self):
        content = UploadDialog(load=self.load_list, cancel=self.dismiss_popup)
        self._popup = Popup(title='Load a file list', content=content, size_hint=(1, 1))
        self._popup.open()

    def load_list(self, path):
        try:
            filename = ('.').join(path[0].split('.')[:-1])
            img = Image.open(path[0])
            r_new = np.uint8(protanopia_filter(0.56667, 0.43333, 0, img))
            g_new = np.uint8(protanopia_filter(0.55833, 0.44167, 0, img))
            b_new = np.uint8(protanopia_filter(0, 0.24167, 0.75833, img))
            rgb = np.dstack((r_new,g_new,b_new))
            new_img = Image.fromarray(rgb, 'RGB')
            new_img.save(str(filename) + '_new.jpg')
            self.ids.image.source = str(filename) + '_new.jpg'
        except: pass

    def dismiss_popup(self):
        self._popup.dismiss()

class About(Screen):
    pass

class ProtanopiaWorld(App):
    def build(self):
        return sm

# multuplying values to get 'protanopia' version of photo
# https://www.cs.cornell.edu/courses/cs1110/2013sp/assignments/assignment3/index.php
def protanopia_filter(R, G, B, img):
    arr = np.array(img)
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    new_color = []
    for i in range(len(r)):
        Rr, Gg, Bb = R * r[i], G * g[i], B * b[i]
        value = Rr + Gg + Bb
        new_color.append(value)
    return new_color

sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(Upload(name='upload'))
sm.add_widget(About(name='about'))

if __name__ == '__main__':
    ProtanopiaWorld().run()
