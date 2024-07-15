from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
import constants

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_image_index = 0
        self.current_theme_index = 0
        self.red_bar_width = 0
        self.yellow_bar_width = 0
        self.piss_button_pressed = False
        self.yellow_bar_decrease_event = None

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
        if button_type == 'piss':
            self.piss_button_pressed = True
            self.start_yellow_bar_decrease_event()
        if button_type == 'punch':
            Clock.schedule_once(self.hide_overlay, 0.1)

    def hide_overlay(self, dt):
        self.overlay_rect.source = ''
        self.overlay_rect.size = (0, 0)
        self.overlay_rect.pos = (0, 0)
        self.stop_yellow_bar_decrease_event()
        self.piss_button_pressed = False

    def start_yellow_bar_decrease_event(self):
        if not self.yellow_bar_decrease_event:
            self.yellow_bar_decrease_event = Clock.schedule_interval(self.decrease_yellow_bar, 0.1)

    def stop_yellow_bar_decrease_event(self):
        if self.yellow_bar_decrease_event:
            self.yellow_bar_decrease_event.cancel()
            self.yellow_bar_decrease_event = None

    def on_touch_piss_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.show_overlay_for_duration('assets/piss.png', touch.pos, 'piss')

    def on_touch_piss_up(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.hide_overlay(0)  # Immediately hide overlay when Piss button is released

    def on_touch_punch(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.decrease_red_bar()
            self.show_overlay_for_duration('assets/punch.png', touch.pos, 'punch')

    def decrease_red_bar(self):
        decrement = 20
        self.red_bar_width -= decrement
        if self.red_bar_width < 0:
            self.red_bar_width = 0
        self.red_bar.size = (self.red_bar_width, 20)

    def decrease_yellow_bar(self, dt):
        if self.piss_button_pressed:
            self.yellow_bar_width -= 15
            if self.yellow_bar_width < 0:
                self.yellow_bar_width = 0
            self.yellow_bar.size = (self.yellow_bar_width, 20)

    def increase_yellow_bar(self, dt):
        overlay_width = self.additional_overlay.size[0] - 20
        self.yellow_bar_width += 5
        if self.yellow_bar_width > overlay_width:
            self.yellow_bar_width = overlay_width 
        self.yellow_bar.size = (self.yellow_bar_width, 20)

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
            Color(1, 1, 1, 0.3)
            overlay_width = Window.size[0] * 1.0
            overlay_height = Window.size[1] * 0.03
            overlay_pos_x = (Window.size[0] - overlay_width) / 2
            overlay_pos_y = Window.size[1] * 0.97
            self.additional_overlay = Rectangle(size=(overlay_width, overlay_height), pos=(overlay_pos_x, overlay_pos_y))
            self.red_bar_width = overlay_width - 20
            bar_y_pos = overlay_pos_y + (overlay_height - 20) / 2

            Color(0.7, 0, 0, 1)
            self.red_bar = Rectangle(size=(self.red_bar_width, 20), pos=(overlay_pos_x + 10, bar_y_pos))

            Color(0.7, 0.7, 0, 0.5)
            self.yellow_bar = Rectangle(size=(self.yellow_bar_width, 20), pos=(overlay_pos_x + 10, bar_y_pos))

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
        self.btn_punch = Button(text='Punch', background_color=constants.mid_btns_color[self.current_theme_index], font_size='50sp')
        self.btn_piss = Button(text='Piss', background_color=constants.mid_btns_color[self.current_theme_index], font_size='50sp')

        self.btn_punch.bind(on_touch_down=self.on_touch_punch)
        self.btn_piss.bind(on_touch_down=self.on_touch_piss_down)
        self.btn_piss.bind(on_touch_up=self.on_touch_piss_up)

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
        Clock.schedule_interval(self.increase_yellow_bar, 0.1)
        return self.main_layout

if __name__ == '__main__':
    MainApp().run()
