from kivymd.app import MDApp
from kivy.lang import Builder
from plyer import filechooser

from kivymd.uix.bottomnavigation import MDBottomNavigationItem

Builder.load_file("home/me/ui.kv")


class MeTap(MDBottomNavigationItem):
    def on_touch_down(self, touch):
        if self.ids:
            if self.ids.user_image.collide_point(*self.to_local(*touch.pos)):
                self.choose_image()
        return super(MeTap, self).on_touch_down(touch)

    def choose_image(self):
        def set_image(files):
            if files:
                self.ids.user_image.source = files[0]
                MDApp.get_running_app().user.update_profile_photo(files[0])

        filechooser.open_file(title="Pic an Image", preview=True, on_selection=set_image,
                              filters=[["Images", "*png", "*jpg", "*webp", '*jpeg', '*jpe', '*gif',
                                       '*pbm', '*pgm', '*ppm', '*bmp', '*ico'], "*"])
