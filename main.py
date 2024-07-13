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
import constants

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_image_index = 0
        self.current_theme_index = 0
        self.red_bar_width = 500  # Initial width of the red bar
        self.yellow_bar_width = 0  # Initial width of the yellow bar

    def change_theme_next(self, instance):
        self.current_theme_index = (self.current_theme_index + 1) % len(constants.background_color)
        self.update_theme()

    def update_theme(self):
        self.main_layout.canvas.before.clear()
        with self.main_layout.canvas.before:
            Color(*constants.background_color[self.current_theme_index])
            self.rect = Rectangle(size=Window.size, pos=self.main_layout.pos)
        for button in [self.left, self.walk, self.right, self.items, self.stats, self.entities, self.censor, self.theme, self.quit]:
            button.background_color = constants.most_buttons_color[self.current_theme_index]
        self.btn_punch.background_color = constants.mid_btns_color[self.current_theme_index]
        self.btn_piss.background_color = constants.mid_btns_color[self.current_theme_index]

    def change_image_next(self, instance):
        self.current_image_index += 1
        if self.current_image_index >= len(constants.PICS):
            self.current_image_index = 0
        self.image.source = constants.PICS[self.current_image_index]
        self.image.reload()

    def update_overlay_image(self, image_path, touch_pos, button_type):
        self.overlay_rect.source = image_path
        self.overlay_rect.size = (self.image.width * 0.5, self.image.height * 0.5)
        overlay_width = self.overlay_rect.size[0]
        overlay_height = self.overlay_rect.size[1]
        if button_type == 'punch':
            self.overlay_rect.pos = (touch_pos[0], touch_pos[1] + overlay_height + overlay_height / 2)
        elif button_type == 'piss':
            self.overlay_rect.pos = (touch_pos[0] - overlay_width, touch_pos[1] + overlay_height + overlay_height / 2)

    def show_overlay_for_duration(self, image_path, touch_pos, button_type):
        self.update_overlay_image(image_path, touch_pos, button_type)
        Clock.schedule_once(self.hide_overlay, 1.0)

    def hide_overlay(self, dt):
        self.overlay_rect.source = ''
        self.overlay_rect.size = (0, 0)
        self.overlay_rect.pos = (0, 0)

    def on_touch_punch(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.decrease_red_bar()
            self.show_overlay_for_duration('assets/punch.png', touch.pos, 'punch')

    def on_touch_piss(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.decrease_yellow_bar()
            self.show_overlay_for_duration('assets/piss.png', touch.pos, 'piss')

    def decrease_red_bar(self):
        self.red_bar_width -= 20  # Decrease the width of the red bar
        if self.red_bar_width < 0:
            self.red_bar_width = 0  # Ensure the width doesn't go negative
        self.red_bar.size = (self.red_bar_width, 20)  # Update the size of the red bar

    def decrease_yellow_bar(self):
        self.yellow_bar_width -= 20  # Decrease the width of the yellow bar
        if self.yellow_bar_width < 0:
            self.yellow_bar_width = 0  # Ensure the width doesn't go negative
        self.yellow_bar.size = (self.yellow_bar_width, 20)  # Update the size of the yellow bar

    def increase_yellow_bar(self, dt):
        self.yellow_bar_width += 10  # Increase the width of the yellow bar
        if self.yellow_bar_width > self.image.width / 1.16:
            self.yellow_bar_width = self.image.width / 1.16  # Ensure the width doesn't exceed the image width
        self.yellow_bar.size = (self.yellow_bar_width, 20)  # Update the size of the yellow bar

    def quit_app(self, instance):
        App.get_running_app().stop()

    def build(self):
        Window.size = (600, 1000)
        self.image = Image(source=constants.PICS[0], size_hint=(1, 0.5), allow_stretch=True)
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        with self.main_layout.canvas.before:
            Color(*constants.background_color[self.current_theme_index])
            self.rect = Rectangle(size=Window.size, pos=self.main_layout.pos)
        self.main_layout.add_widget(self.image)
        
        with self.main_layout.canvas:
            self.overlay_rect = Rectangle(size=self.image.size, pos=self.image.pos)
        
        with self.main_layout.canvas.after:
            Color(1, 0, 0, 1)
            self.red_bar = Rectangle(size=(self.red_bar_width, 20), pos=(50, self.image.pos[1] + self.image.height * 9.7))  # Position above the image
            
            Color(1, 1, 0, 1)  # Yellow color
            self.yellow_bar = Rectangle(size=(self.yellow_bar_width, 20), pos=(50, self.image.pos[1] + self.image.height * 9.5))  # Position above the red bar

        rect_buttons_layout_top = GridLayout(cols=3, size_hint=(1, 0.1), spacing=10)
        self.left = Button(text='Left', background_color=constants.most_buttons_color[self.current_theme_index])
        self.walk = Button(text='Walk', background_color=constants.most_buttons_color[self.current_theme_index])
        self.right = Button(text='Right', background_color=constants.most_buttons_color[self.current_theme_index])
        self.left.bind(on_press=self.change_image_next)
        self.walk.bind(on_press=self.change_image_next)
        self.right.bind(on_press=self.change_image_next)

        rect_buttons_layout_top.add_widget(self.left)
        rect_buttons_layout_top.add_widget(self.walk)
        rect_buttons_layout_top.add_widget(self.right)
        
        self.main_layout.add_widget(rect_buttons_layout_top)
        
        square_buttons_layout = GridLayout(cols=2, size_hint=(1, 0.3), spacing=10)
        self.btn_punch = Button(text='Punch', background_color=constants.mid_btns_color[self.current_theme_index])
        self.btn_piss = Button(text='Piss', background_color=constants.mid_btns_color[self.current_theme_index])
        
        self.btn_punch.bind(on_touch_down=self.on_touch_punch)
        self.btn_piss.bind(on_touch_down=self.on_touch_piss)
        
        square_buttons_layout.add_widget(self.btn_punch)
        square_buttons_layout.add_widget(self.btn_piss)
        
        self.main_layout.add_widget(square_buttons_layout)
        
        rect_buttons_layout_bottom = GridLayout(cols=6, size_hint=(1, 0.05), spacing=10)
        self.items = Button(text='items', size_hint_x=0.7, size_hint_y=0.1, background_color=constants.most_buttons_color[self.current_theme_index])
        self.stats = Button(text='stats', size_hint_x=0.7, size_hint_y=0.1, background_color=constants.most_buttons_color[self.current_theme_index])
        self.entities = Button(text='entities', size_hint_x=0.7, size_hint_y=0.1, background_color=constants.most_buttons_color[self.current_theme_index])
        
        self.censor = Button(text='censor', size_hint_x=0.3, size_hint_y=0.1, background_color=constants.most_buttons_color[self.current_theme_index])
        self.theme = Button(text='theme', size_hint_x=0.3, size_hint_y=0.1, background_color=constants.most_buttons_color[self.current_theme_index])
        self.quit = Button(text='Quit', size_hint_x=0.3, size_hint_y=0.1, background_color=constants.most_buttons_color[self.current_theme_index])
        self.quit.bind(on_press=self.quit_app)
        self.theme.bind(on_press=self.change_theme_next)
        
        rect_buttons_layout_bottom.add_widget(self.items)
        rect_buttons_layout_bottom.add_widget(self.stats)
        rect_buttons_layout_bottom.add_widget(self.entities)
        rect_buttons_layout_bottom.add_widget(self.censor)
        rect_buttons_layout_bottom.add_widget(self.theme)
        rect_buttons_layout_bottom.add_widget(self.quit)
        
        self.main_layout.add_widget(rect_buttons_layout_bottom)
        
        Clock.schedule_interval(self.increase_yellow_bar, 0.3)  # Increase yellow bar width every 0.6 seconds

        return self.main_layout

if __name__ == '__main__':
    MainApp().run()
