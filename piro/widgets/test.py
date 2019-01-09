'''
Rotation Example
================

This example rotates a button using PushMatrix and PopMatrix. You should see
a static button with the words 'hello world' rotated at a 45 degree angle.
'''


from kivy.app import App
from kivy.lang import Builder

kv = '''
FloatLayout:
    canvas:
        Color:
            rgb: 1, 1, 1
        Rectangle:
            pos : 100, 100
            size: 50, 50

    canvas.before:
        PushMatrix
        Rotate:
            angle: 5
            origin: self.center
        Scale:
            x: 2.0

    canvas.after:
        PopMatrix
        
    Button:
        text: 'hello world'
        size_hint: None, None
        pos_hint: {'center_x': .5, 'center_y': .5}
        canvas.before:
            PushMatrix
            Rotate:
                angle: 45
                origin: self.center
        canvas.after:
            PopMatrix
'''


class RotationApp(App):
    def build(self):
        return Builder.load_string(kv)


RotationApp().run()