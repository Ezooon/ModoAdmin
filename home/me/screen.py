from kivy.lang import Builder
from kivymd.uix.bottomnavigation import MDBottomNavigationItem

Builder.load_file("home/me/ui.kv")


class MeTap(MDBottomNavigationItem):
    def on_touch_down(self, touch):
        if self.ids:
            if self.ids.user_image.collide_point(*self.to_local(*touch.pos)):
                self.choose_image()
        return super(MeTap, self).on_touch_down(touch)

    def choose_image(self):
        # use the Plyer library's filechooser if not suitable check its source code if possible to see if you can
        # open the gallery
        pass
