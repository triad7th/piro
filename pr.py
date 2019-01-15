#region environment
# Import kivy config class
from kivy.config import Config
# setup kivy clock as 'free_only'
Config.set('kivy', 'kivy_clock', 'free_only')
#endregion
from kivy.app import App
from kivy.core.window import Window

# piro modules
from piro.widgets.root import PrRoot

class PrApp(App):
    """Main App"""
    def build(self):
        # window size / position
        Window.size = (1024, 768)
        Window.left, Window.top = 300, 200

        # members
        self.pr_root = PrRoot()

        # return
        return self.pr_root

if __name__ == '__main__':
    PrApp().run()
