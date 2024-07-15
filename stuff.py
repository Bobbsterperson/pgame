
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

import constants

def change_theme_next(app):
    app.current_theme_index = (app.current_theme_index + 1) % len(constants.background_color)
    update_theme(app)

def update_theme(app):
    app.main_layout.canvas.before.clear()
    with app.main_layout.canvas.before:
        Color(*constants.background_color[app.current_theme_index])
        app.rect = Rectangle(size=Window.size, pos=app.main_layout.pos)
    for button in [app.left, app.walk, app.right, app.items, app.stats, app.entities, app.censor, app.theme, app.quit]:
        button.background_color = constants.most_buttons_color[app.current_theme_index]
    app.btn_punch.background_color = constants.mid_btns_color[app.current_theme_index]
    app.btn_piss.background_color = constants.mid_btns_color[app.current_theme_index]
