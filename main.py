import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

kivy.require('2.0.0')

class MainApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Add the top square picture
        image = Image(source='your_image.png', size_hint=(1, 0.5))
        main_layout.add_widget(image)
        
        # Add the 3 rectangle buttons below the image
        rect_buttons_layout_top = GridLayout(cols=3, size_hint=(1, 0.1), spacing=10)
        btn1 = Button(text='Left')
        btn2 = Button(text='Walk')
        btn3 = Button(text='Right')
        
        rect_buttons_layout_top.add_widget(btn1)
        rect_buttons_layout_top.add_widget(btn2)
        rect_buttons_layout_top.add_widget(btn3)
        
        main_layout.add_widget(rect_buttons_layout_top)
        
        # Add the 2 bigger square buttons below the rectangle buttons
        square_buttons_layout = GridLayout(cols=2, size_hint=(1, 0.3), spacing=10)
        btn4 = Button(text='Punch')
        btn5 = Button(text='Piss')
        
        square_buttons_layout.add_widget(btn4)
        square_buttons_layout.add_widget(btn5)
        
        main_layout.add_widget(square_buttons_layout)
        
        # Add the 3 rectangle buttons at the bottom
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
