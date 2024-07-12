import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock

kivy.require('2.0.0')

PICS = ['assets/img10.jpg', 'assets/img1.jpg', 'assets/img2.jpg', 'assets/img3.jpg', 'assets/img4.jpg', 'assets/img5.jpg', 'assets/img6.jpg', 'assets/img7.jpg', 'assets/img8.jpg', 'assets/img9.jpg']

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_image_index = 0

    def change_image_next(self, instance):
        self.current_image_index += 1
        if self.current_image_index >= len(PICS):
            self.current_image_index = 0
        self.image.source = PICS[self.current_image_index]
        self.image.reload()

    def update_overlay_image(self, image_path):
        self.overlay_rect.source = image_path
        self.overlay_rect.size = self.image.size
        self.overlay_rect.pos = self.image.pos
        self.image.size = self.overlay_rect.size

    def show_overlay_for_duration(self, image_path):
        self.update_overlay_image(image_path)
        Clock.schedule_once(self.hide_overlay, 1.0)

    def hide_overlay(self, dt):
        self.overlay_rect.source = ''
        self.overlay_rect.size = (0, 0)
        self.overlay_rect.pos = (0, 0)
        self.image.size = Window.size

    def on_touch_punch(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.show_overlay_for_duration('assets/punch.png')
            print(f"Punch button touched at position: {touch.pos}")

    def on_touch_piss(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.show_overlay_for_duration('assets/piss.png')
            print(f"Piss button touched at position: {touch.pos}")

    def build(self):
        Window.size = (600, 1000)
        self.image = Image(source=PICS[0], size_hint=(1, 0.5))
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        with main_layout.canvas.before:
            Color(0.85, 0.3, 0.0, 1.0)
            self.rect = Rectangle(size=Window.size, pos=main_layout.pos)
        
        main_layout.add_widget(self.image)

        with main_layout.canvas:
            self.overlay_rect = Rectangle(size=self.image.size, pos=self.image.pos)
        
        rect_buttons_layout_top = GridLayout(cols=3, size_hint=(1, 0.1), spacing=10)
        btn1 = Button(text='Left')
        btn2 = Button(text='Walk')
        btn3 = Button(text='Right')
        
        btn1.bind(on_press=self.change_image_next)
        btn2.bind(on_press=self.change_image_next)
        btn3.bind(on_press=self.change_image_next)
        
        rect_buttons_layout_top.add_widget(btn1)
        rect_buttons_layout_top.add_widget(btn2)
        rect_buttons_layout_top.add_widget(btn3)
        
        main_layout.add_widget(rect_buttons_layout_top)
        
        square_buttons_layout = GridLayout(cols=2, size_hint=(1, 0.3), spacing=10)
        self.btn_punch = Button(text='Punch')
        self.btn_piss = Button(text='Piss')
        
        self.btn_punch.bind(on_touch_down=self.on_touch_punch)
        self.btn_piss.bind(on_touch_down=self.on_touch_piss)
        
        square_buttons_layout.add_widget(self.btn_punch)
        square_buttons_layout.add_widget(self.btn_piss)
        
        main_layout.add_widget(square_buttons_layout)
        
        rect_buttons_layout_bottom = GridLayout(cols=3, size_hint=(1, 0.05), spacing=10)
        btn6 = Button(text='items')
        btn7 = Button(text='stats')
        btn8 = Button(text='entities')
        
        rect_buttons_layout_bottom.add_widget(btn6)
        rect_buttons_layout_bottom.add_widget(btn7)
        rect_buttons_layout_bottom.add_widget(btn8)
        
        main_layout.add_widget(rect_buttons_layout_bottom)
        
        return main_layout

if __name__ == '__main__':
    MainApp().run()