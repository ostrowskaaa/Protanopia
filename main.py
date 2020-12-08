from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

import time

from android.permissions import request_permissions, Permission
request_permissions([Permission.CAMERA, Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

Builder.load_string("""
<Button>:
    size: 180, 140
    size_hint: None, None  # (0.5,0.5) the widget would be 50% of the parent
    font_size: 15
    color: 0.2, 0.5, 0.6, 1
    background_normal: ''
    background_color: .15, .15, .15, 1

<MenuScreen>:
    FloatLayout:
        BoxLayout:
            Label:
                text: 'welcome to the world\\nof colour blindness'
                text_size: self.width, None
                font_size: 80
                pos_hint: {'center_x': 0.5, 'center_y': .65}
                size_hint: (0.2,0.2)
                padding: (50,50)
        BoxLayout:
            cols: 3

            RelativeLayout:
                ToggleButton:
                    text: 'Upload'
                    font_size: 60
                    size_hint: None,None
                    size: 260, 140
                    pos_hint: {'center_x': 0.45, 'center_y': .35}
                    on_press:
                        root.manager.transition.direction = 'left'
                        root.manager.current = 'upload'
            RelativeLayout:
                Button:
                    text: 'About'
                    font_size: 60
                    size_hint: None,None
                    size: 260, 140
                    pos_hint: {'center_x': 0.5, 'center_y': .35}
                    on_press:
                        root.manager.transition.direction = 'left'
                        root.manager.current = 'about'
            RelativeLayout:
                ToggleButton:
                    text: 'Camera'
                    font_size: 60
                    size_hint: None,None
                    size: 260, 140
                    pos_hint: {'center_x': 0.55, 'center_y': .35}
                    on_press:
                        root.manager.transition.direction = 'left'
                        root.manager.current = 'camera'

        BoxLayout:
            RelativeLayout:
                Button:
                    text: 'Quit'
                    font_size: 80
                    color: 0.7, 0.5, 0.6, 1
                    on_press: app.stop()
                    size_hint: None,None
                    size: 210, 140
                    pos_hint: {'center_x': 0.5, 'center_y': .15}


<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (1920, 1080)
        allow_stretch: True
        play: True
        canvas.before:
            PushMatrix
            Rotate:
                angle: -90
                origin: self.center
        canvas.after:
            PopMatrix
    BoxLayout:
        cols: 2
        RelativeLayout:
            Button:
                text: 'Capture'
                font_size: 50
                size_hint: None, None
            	size: 220, 140
                pos_hint: {'center_x': 0.45, 'center_y': .05}
                on_press: root.capture()
        RelativeLayout:
            Button:
                text: 'Back'
        		font_size: 50
        		size: 220, 140
        		size_hint: None, None
        		pos_hint: {'center_x': 0.65, 'center_y': .05}
        		on_press:
        		    root.manager.transition.direction = 'right'
        		    root.manager.current = 'menu'

<Upload>:
    FloatLayout:
        BoxLayout:
            Image:
                id: image
                size: 640,480
                source: ''
            RelativeLayout:
                Button:
                    text: 'Choose photo'
                    font_size: 70
                    size: 440, 140
                    size_hint: None,None
                    pos_hint: {'center_x': 0.45, 'center_y': .15}
                    on_press: root.show_load_list()

            RelativeLayout:
                Button:
                	text: 'Back'
                    font_size: 80
                    size: 220, 140
                    size_hint: None,None
                    pos_hint: {'center_x': 0.55, 'center_y': .15}
                	on_press:
                	    root.manager.transition.direction = 'right'
                	    root.manager.current = 'menu'

<UploadDialog>:
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserIconView:
            id: filechooser
            rootpath: '/storage/emulated/0/'
    BoxLayout:
        Button:
            text: "Cancel"
            font_size: 80
            size: 220,140
            size_hint: None,None
            pos_hint: {'center_x': 0.55, 'center_y': .05}
            on_press: root.cancel()
        Button:
            text: "Load"
            font_size: 80
            size: 220,140
            size_hint: None,None
            pos_hint: {'center_x': 0.55, 'center_y': .05}
            on_press:
                root.load(filechooser.selection)
                root.cancel()

<About>:
    FloatLayout:
        orientation: 'vertical'
        size: self.parent.size  # important!
        pos: self.parent.pos
        BoxLayout:
            Label:
                text: 'Protanopia is an inability to see the red colour due to the absence of the red retina photoreceptors. It is genetic and affects much more often men than women.\\nThis app goal is to show how people with protanopia see the wolrd.'
                text_size: self.width, None
                font_size: 60
                halign: 'justify'
                pos_hint: {'center_x': 0.5, 'center_y': .65}
                size_hint: (0.2,0.2)
                padding: (40,40)
        BoxLayout:
            RelativeLayout:
                Button:
                    text: 'Back'
                    font_size: 80
                    size: 220, 140
                    size_hint: None, None
                    pos_hint: {'center_x': 0.5, 'center_y': .35}
                    on_press:
                        root.manager.transition.direction = 'right'
                        root.manager.current = 'menu'
""")

class MenuScreen(Screen):
    pass

class CameraClick(Screen):
    def capture(self):
        camera = self.ids['camera']
        timestr = time.strftime('%Y%m%d_%H%M')
        camera.export_to_png('/sdcard/img_{}.png'.format(timestr))

class UploadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Upload(Screen):
        load = ObjectProperty(None)
        cancel = ObjectProperty(None)
        def show_load_list(self):
            content = UploadDialog(load=self.load_list, cancel=self.dismiss_popup)
            self._popup = Popup(title="Load a file list", content=content, size_hint=(1, 1))
            self._popup.open()

        def load_list(self, filename):
            try: self.ids.image.source = filename[0]
            except: pass


        def dismiss_popup(self):
            self._popup.dismiss()

class About(Screen):
    pass

sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(CameraClick(name='camera'))
sm.add_widget(Upload(name='upload'))
sm.add_widget(About(name='about'))

class ProtanopiaWorld(App):
    def build(self):
        #self.icon = 'color-circle.png'
        self.title = 'Colorblindness'
        return sm

if __name__ == '__main__':
    ProtanopiaWorld().run()
