#bouton save history n'affiche rien

"""from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from plyer import notification
from datetime import datetime
import json
import os

# Path to save the step history
HISTORY_FILE = "step_history.json"

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.layout = None
        self.steps_label = None
        self.calories_label = None
        self.date_label = None
        self.weekday_label = None

    def on_pre_enter(self, *args):
        self.build()

    def build(self):
        if not self.layout:
            self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

            # Add a light blue background color
            with self.layout.canvas.before:
                Color(0.678, 0.847, 0.902, 1)  # Light blue color
                self.rect = Rectangle(size=self.size, pos=self.pos)
                self.layout.bind(size=self._update_rect, pos=self._update_rect)

            # Labels
            self.steps_label = Label(text=f"Steps: {self.manager.app.steps}", font_size='32sp', size_hint=(1, None), height=50)
            self.calories_label = Label(text=f"Calories: {self.manager.app.calories:.2f}", font_size='32sp', size_hint=(1, None), height=50)
            self.date_label = Label(text=f"Date: {self.manager.app.date_str}", font_size='32sp', size_hint=(1, None), height=50)
            self.weekday_label = Label(text=f"Day: {self.manager.app.weekday_str}", font_size='32sp', size_hint=(1, None), height=50)

            # Buttons with customized styles
            reset_button = Button(text="Reset", font_size='24sp', size_hint=(1, None), height=60, background_color=(0.502, 0.796, 0.768, 1), color=(1, 1, 1, 1))
            reset_button.bind(on_press=self.manager.app.reset_counter)

            save_history_button = Button(text="Save History", font_size='24sp', size_hint=(1, None), height=60, background_color=(0.502, 0.796, 0.768, 1), color=(1, 1, 1, 1))
            save_history_button.bind(on_press=self.manager.app.save_history)

            history_button = Button(text="History", font_size='24sp', size_hint=(1, None), height=60, background_color=(0.502, 0.796, 0.768, 1), color=(1, 1, 1, 1))
            history_button.bind(on_press=self.show_history)

            # Add widgets to the layout
            self.layout.add_widget(self.steps_label)
            self.layout.add_widget(self.calories_label)
            self.layout.add_widget(self.date_label)
            self.layout.add_widget(self.weekday_label)
            self.layout.add_widget(save_history_button)
            self.layout.add_widget(reset_button)
            self.layout.add_widget(history_button)

            self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def show_history(self, instance):
        self.manager.current = 'history'

class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)
        self.layout = None
        self.build()

    def build(self):
        if not self.layout:
            self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
            
            # Add a light blue background color
            with self.layout.canvas.before:
                Color(0.678, 0.847, 0.902, 1)  # Light blue color
                self.rect = Rectangle(size=self.size, pos=self.pos)
                self.layout.bind(size=self._update_rect, pos=self._update_rect)

            # Title label
            title_label = Label(text="History", font_size='32sp', size_hint=(1, None), height=50)

            # ScrollView for history
            scroll_view = ScrollView(size_hint=(1, None), height=400)

            # Layout for history entries
            history_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=None)
            history_layout.bind(minimum_height=history_layout.setter('height'))

            # Load step history
            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, 'r') as f:
                    history = json.load(f)
                    for date, steps in history.items():
                        history_label = Label(text=f"{date}: {steps} steps", font_size='24sp', size_hint=(1, None), height=50)
                        history_layout.add_widget(history_label)

            scroll_view.add_widget(history_layout)

            # Back button with customized style
            back_button = Button(text="Back", font_size='24sp', size_hint=(1, None), height=60, background_color=(0.502, 0.796, 0.768, 1), color=(1, 1, 1, 1))
            back_button.bind(on_press=self.go_back)

            # Add widgets to the layout
            self.layout.add_widget(title_label)
            self.layout.add_widget(scroll_view)
            self.layout.add_widget(back_button)

            self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def go_back(self, instance):
        self.manager.current = 'home'

class StepCounterApp(App):
    def build(self):
        self.steps = 0
        self.calories = 0.0
        self.start_date = datetime.now()
        self.date_str = self.start_date.strftime("%Y-%m-%d")
        self.weekday_str = self.start_date.strftime("%A")

        self.sm = ScreenManager()
        self.sm.app = self  # Reference to the application

        home_screen = HomeScreen(name='home')
        self.sm.add_widget(home_screen)

        history_screen = HistoryScreen(name='history')
        self.sm.add_widget(history_screen)

        Clock.schedule_interval(self.simulate_steps, 1)
        return self.sm

    def simulate_steps(self, dt):
        self.steps += 1
        self.calories = self.steps * 0.04

        if self.steps % 100 == 0:
            notification.notify(
                title="Step Counter",
                message=f"You have reached {self.steps} steps!",
                timeout=5
            )

        if self.sm.current == 'home':
            home_screen = self.sm.get_screen('home')
            home_screen.steps_label.text = f"Steps: {self.steps}"
            home_screen.calories_label.text = f"Calories: {self.calories:.2f}"
            home_screen.date_label.text = f"Date: {self.date_str}"
            home_screen.weekday_label.text = f"Day: {self.weekday_str}"

    def save_history(self, instance):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
        else:
            history = {}

        history[self.date_str] = self.steps

        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f)

    def reset_counter(self, instance):
        self.steps = 0
        self.calories = 0.0

        if self.sm.current == 'home':
            home_screen = self.sm.get_screen('home')
            home_screen.steps_label.text = f"Steps: {self.steps}"
            home_screen.calories_label.text = f"Calories: {self.calories:.2f}"

if __name__ == '__main__':
    StepCounterApp().run()"""

#avec bouton save history en marche (efa mety)

"""from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from plyer import notification
from datetime import datetime
import json
import os

# Path to save the step history
HISTORY_FILE = "step_history.json"

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.layout = None
        self.steps_label = None
        self.calories_label = None
        self.date_label = None
        self.weekday_label = None

    def on_pre_enter(self, *args):
        self.build()

    def build(self):
        if not self.layout:
            self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

            # Add a light blue background color
            with self.layout.canvas.before:
                Color(0.678, 0.847, 0.902, 1)  # Light blue color
                self.rect = Rectangle(size=self.size, pos=self.pos)
                self.layout.bind(size=self._update_rect, pos=self._update_rect)

            # Labels
            self.steps_label = Label(text=f"Steps: {self.manager.app.steps}", font_size='32sp', size_hint=(1, None), height=50)
            self.calories_label = Label(text=f"Calories: {self.manager.app.calories:.2f}", font_size='32sp', size_hint=(1, None), height=50)
            self.date_label = Label(text=f"Date: {self.manager.app.date_str}", font_size='32sp', size_hint=(1, None), height=50)
            self.weekday_label = Label(text=f"Day: {self.manager.app.weekday_str}", font_size='32sp', size_hint=(1, None), height=50)

            # Buttons with customized styles
            reset_button = Button(text="Reset", font_size='24sp', size_hint=(1, None), height=60, background_color=(0.502, 0.796, 0.768, 1), color=(1, 1, 1, 1))
            reset_button.bind(on_press=self.manager.app.reset_counter)

            save_history_button = Button(text="Save History", font_size='24sp', size_hint=(1, None), height=60, background_color=(0.502, 0.796, 0.768, 1), color=(1, 1, 1, 1))
            save_history_button.bind(on_press=self.manager.app.save_history)

            history_button = Button(text="History", font_size='24sp', size_hint=(1, None), height=60, background_color=(0.502, 0.796, 0.768, 1), color=(1, 1, 1, 1))
            history_button.bind(on_press=self.manager.app.show_history)

            # Add widgets to the layout
            self.layout.add_widget(self.steps_label)
            self.layout.add_widget(self.calories_label)
            self.layout.add_widget(self.date_label)
            self.layout.add_widget(self.weekday_label)
            self.layout.add_widget(save_history_button)
            self.layout.add_widget(reset_button)
            self.layout.add_widget(history_button)

            self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)
        self.layout = None

    def on_pre_enter(self, *args):
        self.build()

    def build(self):
        if not self.layout:
            self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
            
            # Add a light blue background color
            with self.layout.canvas.before:
                Color(0.678, 0.847, 0.902, 1)  # Light blue color
                self.rect = Rectangle(size=self.size, pos=self.pos)
                self.layout.bind(size=self._update_rect, pos=self._update_rect)

            # Title label
            title_label = Label(text="History", font_size='32sp', size_hint=(1, None), height=50)

            # ScrollView for history
            scroll_view = ScrollView(size_hint=(1, None), height=400)

            # Layout for history entries
            history_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=None)
            history_layout.bind(minimum_height=history_layout.setter('height'))

            # Load step history
            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, 'r') as f:
                    history = json.load(f)
                    for date, steps in history.items():
                        history_label = Label(text=f"{date}: {steps} steps", font_size='24sp', size_hint=(1, None), height=50)
                        history_layout.add_widget(history_label)

            scroll_view.add_widget(history_layout)

            # Back button with customized style
            back_button = Button(text="Back", font_size='24sp', size_hint=(1, None), height=60, background_color=(0.502, 0.796, 0.768, 1), color=(1, 1, 1, 1))
            back_button.bind(on_press=self.manager.app.go_back)

            # Add widgets to the layout
            self.layout.add_widget(title_label)
            self.layout.add_widget(scroll_view)
            self.layout.add_widget(back_button)

            self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class StepCounterApp(App):
    def build(self):
        self.steps = 0
        self.calories = 0.0
        self.start_date = datetime.now()
        self.date_str = self.start_date.strftime("%Y-%m-%d")
        self.weekday_str = self.start_date.strftime("%A")

        self.sm = ScreenManager()
        self.sm.app = self  # Reference to the application

        home_screen = HomeScreen(name='home')
        self.sm.add_widget(home_screen)

        history_screen = HistoryScreen(name='history')
        self.sm.add_widget(history_screen)

        Clock.schedule_interval(self.simulate_steps, 1)
        return self.sm

    def simulate_steps(self, dt):
        self.steps += 1
        self.calories = self.steps * 0.04

        if self.steps % 100 == 0:
            notification.notify(
                title="Step Counter",
                message=f"You have reached {self.steps} steps!",
                timeout=5
            )

        if self.sm.current == 'home':
            home_screen = self.sm.get_screen('home')
            home_screen.steps_label.text = f"Steps: {self.steps}"
            home_screen.calories_label.text = f"Calories: {self.calories:.2f}"
            home_screen.date_label.text = f"Date: {self.date_str}"
            home_screen.weekday_label.text = f"Day: {self.weekday_str}"

    def save_history(self, instance):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
        else:
            history = {}

        history[self.date_str] = self.steps

        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f)

        notification.notify(
            title="History Saved",
            message=f"Steps for {self.date_str} have been saved!",
            timeout=5
        )

    def show_history(self, instance):
        self.sm.current = 'history'

    def go_back(self, instance):
        self.sm.current = 'home'

    def reset_counter(self, instance):
        self.steps = 0
        self.calories = 0.0

        if self.sm.current == 'home':
            home_screen = self.sm.get_screen('home')
            home_screen.steps_label.text = f"Steps: {self.steps}"
            home_screen.calories_label.text = f"Calories: {self.calories:.2f}"

if __name__ == '__main__':
    StepCounterApp().run()"""

#avec round boutton (mety 2.0)

"""from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from plyer import notification
from datetime import datetime
import json
import os

# Path to save the step history
HISTORY_FILE = "step_history.json"

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.bind(pos=self.update_rect, size=self.update_rect)
        with self.canvas.before:
            Color(0.5, 0.8, 0.7, 1)  # Button color (80CBC4)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.layout = None
        self.steps_label = None
        self.calories_label = None
        self.date_label = None
        self.weekday_label = None

    def on_pre_enter(self, *args):
        self.build()

    def build(self):
        if not self.layout:
            self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

            # Add a light blue background color
            with self.layout.canvas.before:
                Color(0.678, 0.847, 0.902, 1)  # Light blue color
                self.rect = RoundedRectangle(size=self.size, pos=self.pos)
                self.layout.bind(size=self._update_rect, pos=self._update_rect)

            # Labels
            self.steps_label = Label(text=f"Steps: {self.manager.app.steps}", font_size='32sp', size_hint=(1, None), height=50)
            self.calories_label = Label(text=f"Calories: {self.manager.app.calories:.2f}", font_size='32sp', size_hint=(1, None), height=50)
            self.date_label = Label(text=f"Date: {self.manager.app.date_str}", font_size='32sp', size_hint=(1, None), height=50)
            self.weekday_label = Label(text=f"Day: {self.manager.app.weekday_str}", font_size='32sp', size_hint=(1, None), height=50)

            # Buttons with rounded corners
            reset_button = RoundedButton(text="Reset", font_size='24sp', size_hint=(1, None), height=60)
            reset_button.bind(on_press=self.manager.app.reset_counter)

            save_history_button = RoundedButton(text="Save History", font_size='24sp', size_hint=(1, None), height=60)
            save_history_button.bind(on_press=self.manager.app.save_history)

            history_button = RoundedButton(text="History", font_size='24sp', size_hint=(1, None), height=60)
            history_button.bind(on_press=self.manager.app.show_history)

            # Change button text color to white
            for button in [reset_button, save_history_button, history_button]:
                button.color = (1, 1, 1, 1)

            # Add widgets to the layout
            self.layout.add_widget(self.steps_label)
            self.layout.add_widget(self.calories_label)
            self.layout.add_widget(self.date_label)
            self.layout.add_widget(self.weekday_label)
            self.layout.add_widget(save_history_button)
            self.layout.add_widget(reset_button)
            self.layout.add_widget(history_button)

            self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)
        self.layout = None

    def on_pre_enter(self, *args):
        self.build()

    def build(self):
        if not self.layout:
            self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
            
            # Add a light blue background color
            with self.layout.canvas.before:
                Color(0.678, 0.847, 0.902, 1)  # Light blue color
                self.rect = RoundedRectangle(size=self.size, pos=self.pos)
                self.layout.bind(size=self._update_rect, pos=self._update_rect)

            # Title label
            title_label = Label(text="History", font_size='32sp', size_hint=(1, None), height=50)

            # ScrollView for history
            scroll_view = ScrollView(size_hint=(1, None), height=400)

            # Layout for history entries
            history_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=None)
            history_layout.bind(minimum_height=history_layout.setter('height'))

            # Load step history
            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, 'r') as f:
                    history = json.load(f)
                    for date, steps in history.items():
                        history_label = Label(text=f"{date}: {steps} steps", font_size='24sp', size_hint=(1, None), height=50)
                        history_layout.add_widget(history_label)

            scroll_view.add_widget(history_layout)

            # Back button with rounded corners
            back_button = RoundedButton(text="Back", font_size='24sp', size_hint=(1, None), height=60)
            back_button.bind(on_press=self.manager.app.go_back)

            # Change button text color to white
            back_button.color = (1, 1, 1, 1)

            # Add widgets to the layout
            self.layout.add_widget(title_label)
            self.layout.add_widget(scroll_view)
            self.layout.add_widget(back_button)

            self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class StepCounterApp(App):
    def build(self):
        self.steps = 0
        self.calories = 0.0
        self.start_date = datetime.now()
        self.date_str = self.start_date.strftime("%Y-%m-%d")
        self.weekday_str = self.start_date.strftime("%A")

        self.sm = ScreenManager()
        self.sm.app = self  # Reference to the application

        home_screen = HomeScreen(name='home')
        self.sm.add_widget(home_screen)

        history_screen = HistoryScreen(name='history')
        self.sm.add_widget(history_screen)

        Clock.schedule_interval(self.simulate_steps, 1)
        return self.sm

    def simulate_steps(self, dt):
        self.steps += 1
        self.calories = self.steps * 0.04

        if self.steps % 100 == 0:
            notification.notify(
                title="Step Counter",
                message=f"You have reached {self.steps} steps!",
                timeout=5
            )

        if self.sm.current == 'home':
            home_screen = self.sm.get_screen('home')
            home_screen.steps_label.text = f"Steps: {self.steps}"
            home_screen.calories_label.text = f"Calories: {self.calories:.2f}"
            home_screen.date_label.text = f"Date: {self.date_str}"
            home_screen.weekday_label.text = f"Day: {self.weekday_str}"

    def save_history(self, instance):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
        else:
            history = {}

        history[self.date_str] = self.steps

        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f)

        notification.notify(
            title="History Saved",
            message=f"Steps for {self.date_str} have been saved!",
            timeout=5
        )

    def show_history(self, instance):
        self.sm.current = 'history'

    def go_back(self, instance):
        self.sm.current = 'home'

    def reset_counter(self, instance):
        self.steps = 0
        self.calories = 0.0

        if self.sm.current == 'home':
            home_screen = self.sm.get_screen('home')
            home_screen.steps_label.text = f"Steps: {self.steps}"
            home_screen.calories_label.text = f"Calories: {self.calories:.2f}"

if __name__ == '__main__':
    StepCounterApp().run()"""

#avec boutton rounde 2

"""from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from plyer import notification
from datetime import datetime
import json
import os

# Path to save the step history
HISTORY_FILE = "step_history.json"

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.bind(pos=self.update_rect, size=self.update_rect)
        with self.canvas.before:
            Color(12.8, 12.8, 12.8, 1)  # Default button color
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
        self.color = (0, 0, 0, 1)  # black text color

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def set_background_color(self, color):
        with self.canvas.before:
            Color(*color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.layout = None
        self.steps_label = None
        self.calories_label = None
        self.date_label = None
        self.weekday_label = None

    def on_pre_enter(self, *args):
        self.build()

    def build(self):
        if not self.layout:
            self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

            # Add a light blue background color
            with self.layout.canvas.before:
                Color(0.38, 15.7, 15.3, 1)  # Light blue color
                self.rect = RoundedRectangle(size=self.size, pos=self.pos)
                self.layout.bind(size=self._update_rect, pos=self._update_rect)

            # Labels
            self.steps_label = Label(text=f"Steps: {self.manager.app.steps}", font_size='40sp', size_hint=(1, None), height=50)
            self.calories_label = Label(text=f"Calories: {self.manager.app.calories:.2f}", font_size='40sp', size_hint=(1, None), height=50)
            self.date_label = Label(text=f"Date: {self.manager.app.date_str}", font_size='40sp', size_hint=(1, None), height=50)
            self.weekday_label = Label(text=f"Day: {self.manager.app.weekday_str}", font_size='40sp', size_hint=(1, None), height=50)

            # Buttons with rounded corners
            reset_button = RoundedButton(text="Reset", font_size='24sp', size_hint=(1, None), height=60)
            reset_button.set_background_color((0.5, 0.8, 0.7, 1))
            reset_button.bind(on_press=self.manager.app.reset_counter)

            save_history_button = RoundedButton(text="Save History", font_size='24sp', size_hint=(1, None), height=60)
            save_history_button.set_background_color((0.3, 0.6, 0.9, 1))
            save_history_button.bind(on_press=self.manager.app.save_history)

            history_button = RoundedButton(text="History", font_size='24sp', size_hint=(1, None), height=60)
            history_button.set_background_color((0.7, 0.7, 0.7, 1))
            history_button.bind(on_press=self.manager.app.show_history)

            # Add widgets to the layout
            self.layout.add_widget(self.steps_label)
            self.layout.add_widget(self.calories_label)
            self.layout.add_widget(self.date_label)
            self.layout.add_widget(self.weekday_label)
            self.layout.add_widget(save_history_button)
            self.layout.add_widget(reset_button)
            self.layout.add_widget(history_button)

            self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)
        self.layout = None

    def on_pre_enter(self, *args):
        self.build()

    def build(self):
        if not self.layout:
            self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
            
            # Add a light blue background color
            with self.layout.canvas.before:
                Color(0.38, 15.7, 15.3, 1)  # Light blue color
                self.rect = RoundedRectangle(size=self.size, pos=self.pos)
                self.layout.bind(size=self._update_rect, pos=self._update_rect)

            # Title label
            title_label = Label(text="History", font_size='40sp', size_hint=(1, None), height=50)

            # ScrollView for history
            scroll_view = ScrollView(size_hint=(1, None), height=400)

            # Layout for history entries
            history_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=None)
            history_layout.bind(minimum_height=history_layout.setter('height'))

            # Load step history
            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, 'r') as f:
                    history = json.load(f)
                    for date, steps in history.items():
                        history_label = Label(text=f"{date}: {steps} steps", font_size='24sp', size_hint=(1, None), height=50)
                        history_layout.add_widget(history_label)

            scroll_view.add_widget(history_layout)

            # Back button with rounded corners
            back_button = RoundedButton(text="Back", font_size='24sp', size_hint=(1, None), height=60)
            back_button.set_background_color((0.7, 0.7, 0.7, 1))
            back_button.bind(on_press=self.manager.app.go_back)

            # Add widgets to the layout
            self.layout.add_widget(title_label)
            self.layout.add_widget(scroll_view)
            self.layout.add_widget(back_button)

            self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class StepCounterApp(App):
    def build(self):
        self.steps = 0
        self.calories = 0.0
        self.start_date = datetime.now()
        self.date_str = self.start_date.strftime("%Y-%m-%d")
        self.weekday_str = self.start_date.strftime("%A")

        self.sm = ScreenManager()
        self.sm.app = self  # Reference to the application

        home_screen = HomeScreen(name='home')
        self.sm.add_widget(home_screen)

        history_screen = HistoryScreen(name='history')
        self.sm.add_widget(history_screen)

        Clock.schedule_interval(self.simulate_steps, 1)
        return self.sm

    def simulate_steps(self, dt):
        self.steps += 1
        self.calories = self.steps * 0.04

        if self.steps % 100 == 0:
            notification.notify(
                title="Step Counter",
                message=f"You have reached {self.steps} steps!",
                timeout=5
            )

        if self.sm.current == 'home':
            home_screen = self.sm.get_screen('home')
            home_screen.steps_label.text = f"Steps: {self.steps}"
            home_screen.calories_label.text = f"Calories: {self.calories:.2f}"
            home_screen.date_label.text = f"Date: {self.date_str}"
            home_screen.weekday_label.text = f"Day: {self.weekday_str}"

    def save_history(self, instance):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
        else:
            history = {}

        history[self.date_str] = self.steps

        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f)

        notification.notify(
            title="History Saved",
            message=f"Steps for {self.date_str} have been saved!",
            timeout=5
        )

    def show_history(self, instance):
        self.sm.current = 'history'

    def go_back(self, instance):
        self.sm.current = 'home'

    def reset_counter(self, instance):
        self.steps = 0
        self.calories = 0.0

        if self.sm.current == 'home':
            home_screen = self.sm.get_screen('home')
            home_screen.steps_label.text = f"Steps: {self.steps}"
            home_screen.calories_label.text = f"Calories: {self.calories:.2f}"

if __name__ == '__main__':
    StepCounterApp().run()"""

#supr bouton par déf

"""from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from plyer import notification
from datetime import datetime
import json
import os

# Path to save the step history
HISTORY_FILE = "step_history.json"

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.bind(pos=self.update_rect, size=self.update_rect)
        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)  # Default button color (gray)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
        self.color = (0, 0, 0, 1)  # black text color

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def set_background_color(self, color):
        with self.canvas.before:
            Color(*color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.layout = None
        self.steps_label = None
        self.calories_label = None
        self.date_label = None
        self.weekday_label = None

    def on_pre_enter(self, *args):
        self.build()

    def build(self):
        if not self.layout:
            self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

            # Add a light blue background color
            with self.layout.canvas.before:
                Color(0.678, 0.847, 0.902, 1)  # Light blue color
                self.rect = RoundedRectangle(size=self.size, pos=self.pos)
                self.layout.bind(size=self._update_rect, pos=self._update_rect)

            # Labels
            self.steps_label = Label(text=f"Steps: {self.manager.app.steps}", font_size='40sp', size_hint=(1, None), height=50)
            self.calories_label = Label(text=f"Calories: {self.manager.app.calories:.2f}", font_size='40sp', size_hint=(1, None), height=50)
            self.date_label = Label(text=f"Date: {self.manager.app.date_str}", font_size='40sp', size_hint=(1, None), height=50)
            self.weekday_label = Label(text=f"Day: {self.manager.app.weekday_str}", font_size='40sp', size_hint=(1, None), height=50)

            # Buttons with rounded corners
            reset_button = RoundedButton(text="Reset", font_size='24sp', size_hint=(1, None), height=60)
            reset_button.set_background_color((0.5, 0.8, 0.7, 1))
            reset_button.bind(on_press=self.manager.app.reset_counter)

            save_history_button = RoundedButton(text="Save History", font_size='24sp', size_hint=(1, None), height=60)
            save_history_button.set_background_color((0.3, 0.6, 0.9, 1))
            save_history_button.bind(on_press=self.manager.app.save_history)

            history_button = RoundedButton(text="History", font_size='24sp', size_hint=(1, None), height=60)
            history_button.set_background_color((0.7, 0.7, 0.7, 1))
            history_button.bind(on_press=self.manager.app.show_history)

            # Add widgets to the layout
            self.layout.add_widget(self.steps_label)
            self.layout.add_widget(self.calories_label)
            self.layout.add_widget(self.date_label)
            self.layout.add_widget(self.weekday_label)
            self.layout.add_widget(save_history_button)
            self.layout.add_widget(reset_button)
            self.layout.add_widget(history_button)

            self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)
        self.layout = None

    def on_pre_enter(self, *args):
        self.build()

    def build(self):
        if not self.layout:
            self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
            
            # Add a light blue background color
            with self.layout.canvas.before:
                Color(0.678, 0.847, 0.902, 1)  # Light blue color
                self.rect = RoundedRectangle(size=self.size, pos=self.pos)
                self.layout.bind(size=self._update_rect, pos=self._update_rect)

            # Title label
            title_label = Label(text="History", font_size='40sp', size_hint=(1, None), height=50)

            # ScrollView for history
            scroll_view = ScrollView(size_hint=(1, None), height=400)

            # Layout for history entries
            history_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=None)
            history_layout.bind(minimum_height=history_layout.setter('height'))

            # Load step history
            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, 'r') as f:
                    history = json.load(f)
                    for date, steps in history.items():
                        history_label = Label(text=f"{date}: {steps} steps", font_size='24sp', size_hint=(1, None), height=50)
                        history_layout.add_widget(history_label)

            scroll_view.add_widget(history_layout)

            # Back button with rounded corners
            back_button = RoundedButton(text="Back", font_size='24sp', size_hint=(1, None), height=60)
            back_button.set_background_color((0.7, 0.7, 0.7, 1))
            back_button.bind(on_press=self.manager.app.go_back)

            # Add widgets to the layout
            self.layout.add_widget(title_label)
            self.layout.add_widget(scroll_view)
            self.layout.add_widget(back_button)

            self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class StepCounterApp(App):
    def build(self):
        self.steps = 0
        self.calories = 0.0
        self.start_date = datetime.now()
        self.date_str = self.start_date.strftime("%Y-%m-%d")
        self.weekday_str = self.start_date.strftime("%A")

        self.sm = ScreenManager()
        self.sm.app = self  # Reference to the application

        home_screen = HomeScreen(name='home')
        self.sm.add_widget(home_screen)

        history_screen = HistoryScreen(name='history')
        self.sm.add_widget(history_screen)

        Clock.schedule_interval(self.simulate_steps, 1)
        return self.sm

    def simulate_steps(self, dt):
        self.steps += 1
        self.calories = self.steps * 0.04

        if self.steps % 100 == 0:
            notification.notify(
                title="Step Counter",
                message=f"You have reached {self.steps} steps!",
                timeout=5
            )

        if self.sm.current == 'home':
            home_screen = self.sm.get_screen('home')
            home_screen.steps_label.text = f"Steps: {self.steps}"
            home_screen.calories_label.text = f"Calories: {self.calories:.2f}"
            home_screen.date_label.text = f"Date: {self.date_str}"
            home_screen.weekday_label.text = f"Day: {self.weekday_str}"

    def save_history(self, instance):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
        else:
            history = {}

        history[self.date_str] = self.steps

        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f)

        notification.notify(
            title="History Saved",
            message=f"Steps for {self.date_str} have been saved!",
            timeout=5
        )

    def show_history(self, instance):
        self.sm.current = 'history'

    def go_back(self, instance):
        self.sm.current = 'home'

    def reset_counter(self, instance):
        self.steps = 0
        self.calories = 0.0

        if self.sm.current == 'home':
            home_screen = self.sm.get_screen('home')
            home_screen.steps_label.text = f"Steps: {self.steps}"
            home_screen.calories_label.text = f"Calories: {self.calories:.2f}"

if __name__ == '__main__':
    StepCounterApp().run()"""

#Avec KV efa mety be bain a

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
#from kivymd.utils.fitimage import dp
from kivy.metrics import dp
from plyer import notification
from datetime import datetime
import json
import os

# Path to save the step history
HISTORY_FILE = "step_history.json"

KV = '''
<HomeScreen>:
    name: 'home'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        canvas.before:
            Color:
                rgba: 0.678, 0.847, 0.902, 1  # Light blue color
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [20]

        MDLabel:
            id: steps_label
            text: "Steps: 0"
            halign: 'center'
            font_style: 'H3'
            size_hint_y: None
            height: self.texture_size[1]

        MDLabel:
            id: calories_label
            text: "Calories: 0.00"
            halign: 'center'
            font_style: 'H3'
            size_hint_y: None
            height: self.texture_size[1]

        MDLabel:
            id: date_label
            text: "Date: "
            halign: 'center'
            font_style: 'H3'
            size_hint_y: None
            height: self.texture_size[1]

        MDLabel:
            id: weekday_label
            text: "Day: "
            halign: 'center'
            font_style: 'H3'
            size_hint_y: None
            height: self.texture_size[1]

        MDRoundFlatButton:
            text: "Save History"
            font_size: '24sp'
            size_hint_y: None
            height: dp(60)
            md_bg_color: 0.3, 0.6, 0.9, 1
            pos_hint: {"center_x": 0.5}
            on_press: app.save_history()

        MDRoundFlatButton:
            text: "Reset"
            font_size: '24sp'
            size_hint_y: None
            height: dp(60)
            md_bg_color: 0.5, 0.8, 0.7, 1
            pos_hint: {"center_x": 0.5}
            on_press: app.reset_counter()

        MDRoundFlatButton:
            text: "History"
            font_size: '24sp'
            size_hint_y: None
            height: dp(60)
            md_bg_color: 0.7, 0.7, 0.7, 1
            pos_hint: {"center_x": 0.5}
            on_press: app.show_history()

<HistoryScreen>:
    name: 'history'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        canvas.before:
            Color:
                rgba: 0.678, 0.847, 0.902, 1  # Light blue color
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [20]

        MDLabel:
            text: "History"
            halign: 'center'
            font_style: 'H3'
            size_hint_y: None
            height: self.texture_size[1]

        ScrollView:
            size_hint: (1, None)
            height: dp(400)

            BoxLayout:
                id: history_layout
                orientation: 'vertical'
                padding: dp(10)
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height

        MDRoundFlatButton:
            text: "Back"
            font_size: '24sp'
            size_hint_y: None
            height: dp(60)
            md_bg_color: 0.7, 0.7, 0.7, 1
            pos_hint: {"center_x": 0.5}
            on_press: app.go_back()
'''

class HomeScreen(Screen):
    pass

class HistoryScreen(Screen):
    pass

class StepCounterApp(MDApp):
    def build(self):
        #charger le fichier KV
        Builder.load_string(KV)

        self.steps = 0
        self.calories = 0.0
        self.start_date = datetime.now()
        self.date_str = self.start_date.strftime("%Y-%m-%d")
        self.weekday_str = self.start_date.strftime("%A")

        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(HistoryScreen(name='history'))

        Clock.schedule_interval(self.simulate_steps, 1)
        return self.sm #Builder.load_string(KV)

    def simulate_steps(self, dt):
        self.steps += 1
        self.calories = self.steps * 0.04

        if self.steps % 100 == 0:
            notification.notify(
                title="Step Counter",
                message=f"You have reached {self.steps} steps!",
                timeout=5
            )

        if self.sm.current == 'home':
            home_screen = self.sm.get_screen('home')
            home_screen.ids.steps_label.text = f"Steps: {self.steps}"
            home_screen.ids.calories_label.text = f"Calories: {self.calories:.2f}"
            home_screen.ids.date_label.text = f"Date: {self.date_str}"
            home_screen.ids.weekday_label.text = f"Day: {self.weekday_str}"

    def save_history(self):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
        else:
            history = {}

        history[self.date_str] = self.steps

        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f)

        notification.notify(
            title="History Saved",
            message=f"Steps for {self.date_str} have been saved!",
            timeout=5
        )

    def show_history(self):
        self.sm.current = 'history'
        history_screen = self.sm.get_screen('history')
        history_layout = history_screen.ids.history_layout
        history_layout.clear_widgets()

        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
                for date, steps in history.items():
                    history_label = MDLabel(text=f"{date}: {steps} steps", font_style='H5', size_hint_y=None, height=dp(50))
                    history_layout.add_widget(history_label)

    def go_back(self):
        self.sm.current = 'home'

    def reset_counter(self):
        self.steps = 0
        self.calories = 0.0

        if self.sm.current == 'home':
            home_screen = self.sm.get_screen('home')
            home_screen.ids.steps_label.text = f"Steps: {self.steps}"
            home_screen.ids.calories_label.text = f"Calories: {self.calories:.2f}"

if __name__ == '__main__':
    StepCounterApp().run()

#Avec accelerometer
"""from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
#from kivymd.utils.fitimage import dp
from kivy.metrics import dp
from plyer import notification
from datetime import datetime
import json
import os

# Import the accelerometer module
from plyer import accelerometer

# Path to save the step history
HISTORY_FILE = "step_history.json"

KV = '''
<HomeScreen>:
    name: 'home'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        canvas.before:
            Color:
                rgba: 0.678, 0.847, 0.902, 1  # Light blue color
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [20]

        MDLabel:
            id: steps_label
            text: "Steps: 0"
            halign: 'center'
            font_style: 'H3'
            size_hint_y: None
            height: self.texture_size[1]

        MDLabel:
            id: calories_label
            text: "Calories: 0.00"
            halign: 'center'
            font_style: 'H3'
            size_hint_y: None
            height: self.texture_size[1]

        MDLabel:
            id: date_label
            text: "Date: "
            halign: 'center'
            font_style: 'H3'
            size_hint_y: None
            height: self.texture_size[1]

        MDLabel:
            id: weekday_label
            text: "Day: "
            halign: 'center'
            font_style: 'H3'
            size_hint_y: None
            height: self.texture_size[1]

        MDRoundFlatButton:
            text: "Save History"
            font_size: '24sp'
            size_hint_y: None
            height: dp(60)
            md_bg_color: 0.3, 0.6, 0.9, 1
            pos_hint: {"center_x": 0.5}
            on_press: app.save_history()

        MDRoundFlatButton:
            text: "Reset"
            font_size: '24sp'
            size_hint_y: None
            height: dp(60)
            md_bg_color: 0.5, 0.8, 0.7, 1
            pos_hint: {"center_x": 0.5}
            on_press: app.reset_counter()

        MDRoundFlatButton:
            text: "History"
            font_size: '24sp'
            size_hint_y: None
            height: dp(60)
            md_bg_color: 0.7, 0.7, 0.7, 1
            pos_hint: {"center_x": 0.5}
            on_press: app.show_history()

<HistoryScreen>:
    name: 'history'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        canvas.before:
            Color:
                rgba: 0.678, 0.847, 0.902, 1  # Light blue color
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [20]

        MDLabel:
            text: "History"
            halign: 'center'
            font_style: 'H3'
            size_hint_y: None
            height: self.texture_size[1]

        ScrollView:
            size_hint: (1, None)
            height: dp(400)

            BoxLayout:
                id: history_layout
                orientation: 'vertical'
                padding: dp(10)
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height

        MDRoundFlatButton:
            text: "Back"
            font_size: '24sp'
            size_hint_y: None
            height: dp(60)
            md_bg_color: 0.7, 0.7, 0.7, 1
            pos_hint: {"center_x": 0.5}
            on_press: app.go_back()
'''

class HomeScreen(Screen):
    pass

class HistoryScreen(Screen):
    pass

class StepCounterApp(MDApp):
    def build(self):
        #charger le fichier KV
        Builder.load_string(KV)

        self.steps = 0
        self.calories = 0.0
        self.start_date = datetime.now()
        self.date_str = self.start_date.strftime("%Y-%m-%d")
        self.weekday_str = self.start_date.strftime("%A")

        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(HistoryScreen(name='history'))

        # Start the accelerometer
        accelerometer.enable()

        Clock.schedule_interval(self.simulate_steps, 1)
        return self.sm #Builder.load_string(KV)

    def simulate_steps(self, dt):
        # Get the acceleration data
        acceleration = accelerometer.acceleration[:3]

        # Calculate steps based on acceleration data (this is just a placeholder)
        self.steps += sum(map(abs, acceleration))

        self.calories = self.steps * 0.04

        if self.steps % 100 == 0:
            notification.notify(
                title="Step Counter",
                message=f"You have reached {self.steps} steps!",
                timeout=5
            )

        if self.sm.current == 'home':
            home_screen = self.sm.get_screen('home')
            home_screen.ids.steps_label.text = f"Steps: {self.steps}"
            home_screen.ids.calories_label.text = f"Calories: {self.calories:.2f}"
            home_screen.ids.date_label.text = f"Date: {self.date_str}"
            home_screen.ids.weekday_label.text = f"Day: {self.weekday_str}"

    def save_history(self):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
        else:
            history = {}

        history[self.date_str] = self.steps

        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f)

        notification.notify(
            title="History Saved",
            message=f"Steps for {self.date_str} have been saved!",
            timeout=5
        )

    def show_history(self):
        self.sm.current = 'history'
        history_screen = self.sm.get_screen('history')
        history_layout = history_screen.ids.history_layout
        history_layout.clear_widgets()

        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
                for date, steps in history.items():
                    history_label = MDLabel(text=f"{date}: {steps} steps", font_style='H5', size_hint_y=None, height=dp(50))
                    history_layout.add_widget(history_label)

    def go_back(self):
        self.sm.current = 'home'

    def reset_counter(self):
        self.steps = 0
        self.calories = 0.0

        if self.sm.current == 'home':
            home_screen = self.sm.get_screen('home')
            home_screen.ids.steps_label.text = f"Steps: {self.steps}"
            home_screen.ids.calories_label.text = f"Calories: {self.calories:.2f}"

if __name__ == '__main__':
    StepCounterApp().run()
"""


#simulation avec react native
"""import React, { useState, useEffect } from 'react';
import { View, Text, Button, ScrollView } from 'react-native';
import { Notification } from 'react-native-push-notification';
import AsyncStorage from '@react-native-async-storage/async-storage';

const HISTORY_FILE = "step_history.json";

const HomeScreen = ({ steps, calories, dateStr, weekdayStr, onSaveHistory, onResetCounter, onShowHistory }) => {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 }}>
      <Text>Steps: {steps}</Text>
      <Text>Calories: {calories.toFixed(2)}</Text>
      <Text>Date: {dateStr}</Text>
      <Text>Day: {weekdayStr}</Text>
      <Button title="Save History" onPress={onSaveHistory} />
      <Button title="Reset" onPress={onResetCounter} />
      <Button title="History" onPress={onShowHistory} />
    </View>
  );
};

const HistoryScreen = ({ history }) => {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 }}>
      <Text>History</Text>
      <ScrollView>
        {history.map((entry, index) => (
          <Text key={index}>{entry.date}: {entry.steps} steps</Text>
        ))}
      </ScrollView>
      <Button title="Back" onPress={onGoBack} />
    </View>
  );
};

const StepCounterApp = () => {
  const [steps, setSteps] = useState(0);
  const [calories, setCalories] = useState(0.0);
  const [dateStr, setDateStr] = useState('');
  const [weekdayStr, setWeekdayStr] = useState('');
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const intervalId = setInterval(() => {
      setSteps(prevSteps => prevSteps + 1);
      setCalories(prevCalories => prevCalories + 0.04);

      if (steps % 100 === 0) {
        Notification.localNotification({
          title: "Step Counter",
          message: `You have reached ${steps} steps!`,
          channelId: "step-counter-channel",
        });
      }
    }, 1000);

    return () => clearInterval(intervalId);
  }, [steps]);

  const onSaveHistory = async () => {
    const newEntry = { date: dateStr, steps };
    const updatedHistory = [...history, newEntry];
    setHistory(updatedHistory);

    try {
      await AsyncStorage.setItem(HISTORY_FILE, JSON.stringify(updatedHistory));
      Notification.localNotification({
        title: "History Saved",
        message: `Steps for ${dateStr} have been saved!`,
        channelId: "step-counter-channel",
      });
    } catch (error) {
      console.error('Error saving history:', error);
    }
  };

  const onShowHistory = async () => {
    try {
      const historyData = await AsyncStorage.getItem(HISTORY_FILE);
      if (historyData !== null) {
        setHistory(JSON.parse(historyData));
      }
    } catch (error) {
      console.error('Error retrieving history:', error);
    }
  };

  const onResetCounter = () => {
    setSteps(0);
    setCalories(0.0);
  };

  const onGoBack = () => {
    // Go back to previous screen
  };

  return (
    <HomeScreen
      steps={steps}
      calories={calories}
      dateStr={dateStr}
      weekdayStr={weekdayStr}
      onSaveHistory={onSaveHistory}
      onResetCounter={onResetCounter}
      onShowHistory={onShowHistory}
    />
  );
};

export default StepCounterApp;
"""


#React native avec accelerometer
"""import React, { useState, useEffect } from 'react';
import { View, Text, Button, ScrollView } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Accelerometer } from 'expo-sensors';
import { Notifications } from 'expo';

const HISTORY_FILE = "step_history.json";

const HomeScreen = ({ steps, calories, dateStr, weekdayStr, onSaveHistory, onResetCounter, onShowHistory }) => {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 }}>
      <Text>Steps: {steps}</Text>
      <Text>Calories: {calories.toFixed(2)}</Text>
      <Text>Date: {dateStr}</Text>
      <Text>Day: {weekdayStr}</Text>
      <Button title="Save History" onPress={onSaveHistory} />
      <Button title="Reset" onPress={onResetCounter} />
      <Button title="History" onPress={onShowHistory} />
    </View>
  );
};

const HistoryScreen = ({ history }) => {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 }}>
      <Text>History</Text>
      <ScrollView>
        {history.map((entry, index) => (
          <Text key={index}>{entry.date}: {entry.steps} steps</Text>
        ))}
      </ScrollView>
      <Button title="Back" onPress={onGoBack} />
    </View>
  );
};

const StepCounterApp = () => {
  const [steps, setSteps] = useState(0);
  const [calories, setCalories] = useState(0.0);
  const [dateStr, setDateStr] = useState('');
  const [weekdayStr, setWeekdayStr] = useState('');
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const subscription = Accelerometer.addListener(data => {
      const acceleration = data.acceleration;
      const newSteps = steps + Math.abs(acceleration.x) + Math.abs(acceleration.y) + Math.abs(acceleration.z);
      setSteps(newSteps);
      setCalories(newSteps * 0.04);

      if (newSteps % 100 === 0) {
        Notifications.presentLocalNotificationAsync({
          title: "Step Counter",
          body: `You have reached ${newSteps} steps!`,
        });
      }
    });

    return () => {
      subscription.remove();
    };
  }, [steps]);

  const onSaveHistory = async () => {
    const newEntry = { date: dateStr, steps };
    const updatedHistory = [...history, newEntry];
    setHistory(updatedHistory);

    try {
      await AsyncStorage.setItem(HISTORY_FILE, JSON.stringify(updatedHistory));
      Notifications.presentLocalNotificationAsync({
        title: "History Saved",
        body: `Steps for ${dateStr} have been saved!`,
      });
    } catch (error) {
      console.error('Error saving history:', error);
    }
  };

  const onShowHistory = async () => {
    try {
      const historyData = await AsyncStorage.getItem(HISTORY_FILE);
      if (historyData !== null) {
        setHistory(JSON.parse(historyData));
      }
    } catch (error) {
      console.error('Error retrieving history:', error);
    }
  };

  const onResetCounter = () => {
    setSteps(0);
    setCalories(0.0);
  };

  const onGoBack = () => {
    // Go back to previous screen
  };

  return (
    <HomeScreen
      steps={steps}
      calories={calories}
      dateStr={dateStr}
      weekdayStr={weekdayStr}
      onSaveHistory={onSaveHistory}
      onResetCounter={onResetCounter}
      onShowHistory={onShowHistory}
    />
  );
};

export default StepCounterApp;
"""
"""import { useEffect } from 'react';
import { Accelerometer } from 'expo-sensors';
import { Permissions } from 'expo';

const StepCounterApp = () => {
  useEffect(() => {
    const requestPermissions = async () => {
      const { status } = await Permissions.askAsync(Permissions.ACCELEROMETER);
      if (status !== 'granted') {
        console.log('Permission to access accelerometer denied');
      }
    };

    requestPermissions();
  }, []);

  // Reste du code...
};
"""








