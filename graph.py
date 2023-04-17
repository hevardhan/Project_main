from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

x = [1, 2, 3, 4]
y = [5, 10, 12, 9]

plt.plot(x, y)

plt.ylabel("Y axis")
plt.xlabel("X axis")


class Demo(FloatLayout):
    def _init_(self, **kwargs):
        super()._init_(**kwargs)
        box = self.ids.box
        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))


class Main(App):
    def build(self):
        Builder.load_file("kv/graph.kv")
        return Demo()


Main().run()