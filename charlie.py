import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
class MyApp (object):

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("groupMessage.glade")
        self.builder.connect_signals(self)

    def run(self):
        self.builder.get_object("window").show_all()
        Gtk.main()

    def on_window_destroy(self, *args):
        Gtk.main_quit()

    def on_button1_clicked(self, *args):
    	item1=self.builder.get_object("entry4")
    	print item1.get_text()


MyApp().run()