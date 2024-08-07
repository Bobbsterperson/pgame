from kivy.core.audio import SoundLoader


text_left = """
                maybe for taking
                turns but
                for accepting or
                denying quests
                """
text_right = "Look right."



PICS = ['assets/img1.jpg', 'assets/img2.jpg', 'assets/img3.jpg', 'assets/img4.jpg', 'assets/img5.jpg', 'assets/img6.jpg', 'assets/img7.jpg', 'assets/img8.jpg', 'assets/img9.jpg']
PISS = ['assets/piss.png', 'assets/piss4.png', 'assets/piss6.png', 'assets/piss7.png', 'assets/piss8.png']
# , 'assets/piss2.png'
#  'assets/piss5.png',
# , 'assets/piss9.png'
#  'assets/piss3.png',
background_color = [
                    (0.3, 0.3, 0.3, 1.0),
                    (0.2, 0.1, 0.2, 1.0),
                    (0.1, 0.2, 0.4, 1.0),
                    (0.5, 0.2, 0.1, 1.0),
                    (0.1, 0.3, 0.4, 1.0),
                    (0.4, 0.4, 0.2, 1.0),
                    (0.2, 0.6, 0.6, 1.0)
                    ]
most_buttons_color = [
                      (0.5, 0.3, 0.2, 1),
                      (0.3, 0.5, 0.0, 1),
                      (0.1, 0.6, 0.4, 1),
                      (0.8, 0.4, 0.0, 1),
                      (0.2, 0.6, 0.4, 1),
                      (0.7, 0.1, 0.3, 1),
                      (0.5, 0.2, 0.8, 1),
                      ]
mid_btns_color = [
                  (0.5, 0.2, 0.3, 1),
                  (0.3, 0.5, 0.4, 1),
                  (0.2, 0.7, 0.5, 1),
                  (0.2, 0.7, 0.8, 1),
                  (0.1, 0.4, 0.9, 1),
                  (0.6, 0.2, 0.5, 1),
                  (0.8, 0.3, 0.7, 1),
                  ]


PISS_SOUND_PATH = 'assets/piss.wav'
PUNCH_SOUND_PATH = 'assets/punch.wav'
piss_sound = SoundLoader.load(PISS_SOUND_PATH)
punch_sound = SoundLoader.load(PUNCH_SOUND_PATH)