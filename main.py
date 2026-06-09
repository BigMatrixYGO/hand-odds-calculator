from math import comb
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout


# ---------------- FUNCTIONS ---------------- #

def specific_hand_probability(a, x, n, h):
    return round((comb(a, x) * comb(n - a, h - x)) / comb(n, h), 4)


def at_least_one_target_probability(a, n, h):
    return round(1 - (comb(n - a, h) / comb(n, h)), 4)


def dual_target_probability(a1, x1, a2, x2, n, h):

    if x1 + x2 > h:
        return 0

    return round(
        (
            comb(a1, x1)
            * comb(a2, x2)
            * comb(n - a1 - a2, h - x1 - x2)
        )
        / comb(n, h),
        4,
    )


def at_least_one_each_target(a1, a2, n, h):

    total = comb(n, h)

    none = comb(n - a1 - a2, h)

    only_a1 = (
        comb(a1, 1)
        * comb(n - a1 - a2, h - 1)
        if h >= 1 else 0
    )

    only_a2 = (
        comb(a2, 1)
        * comb(n - a1 - a2, h - 1)
        if h >= 1 else 0
    )

    valid = total - none - only_a1 - only_a2

    return round(valid / total, 4)


# ---------------- APP ---------------- #

class ProbabilityApp(App):

    def build(self):

        self.history = []

        root = BoxLayout(
            orientation='vertical',
            padding=15,
            spacing=10
        )

        title = Label(
            text="Card Probability Calculator",
            font_size=30,
            size_hint=(1, 0.12)
        )

        root.add_widget(title)

        self.spinner = Spinner(
            text='Select Function',
            values=(
                '1 - Exact Target Cards',
                '2 - At Least One Target',
                '3 - Exact Dual Targets',
                '4 - At Least One Of Each'
            ),
            size_hint=(1, 0.1)
        )

        self.spinner.bind(text=self.update_inputs)

        root.add_widget(self.spinner)

        self.inputs_box = BoxLayout(
            orientation='vertical',
            spacing=8,
            size_hint=(1, 0.35)
        )

        root.add_widget(self.inputs_box)

        calculate_button = Button(
            text="Calculate",
            font_size=24,
            size_hint=(1, 0.1)
        )

        calculate_button.bind(on_press=self.calculate)

        root.add_widget(calculate_button)

        clear_button = Button(
            text="Clear History",
            font_size=20,
            size_hint=(1, 0.08)
        )

        clear_button.bind(on_press=self.clear_history)

        root.add_widget(clear_button)

        self.result_label = Label(
            text="Result...",
            font_size=24,
            size_hint=(1, 0.1)
        )

        root.add_widget(self.result_label)

        history_title = Label(
            text="Calculation History",
            font_size=24,
            size_hint=(1, 0.08)
        )

        root.add_widget(history_title)

        scroll = ScrollView(size_hint=(1, 0.35))

        self.history_layout = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None
        )

        self.history_layout.bind(
            minimum_height=self.history_layout.setter('height')
        )

        scroll.add_widget(self.history_layout)

        root.add_widget(scroll)

        self.fields = {}

        return root

    # ---------------- INPUTS ---------------- #

    def create_input(self, key, hint):

        txt = TextInput(
            hint_text=hint,
            multiline=False,
            input_filter='int',
            font_size=22,
            size_hint=(1, None),
            height=80
        )

        self.fields[key] = txt

        self.inputs_box.add_widget(txt)

    def update_inputs(self, spinner, text):

        self.inputs_box.clear_widgets()

        self.fields = {}

        if text.startswith("1"):

            self.create_input("n", "Deck Size")
            self.create_input("a", "Target Cards")
            self.create_input("x", "Desired Targets In Hand")
            self.create_input("h", "Opening Hand Size")

        elif text.startswith("2"):

            self.create_input("n", "Deck Size")
            self.create_input("a", "Target Cards")
            self.create_input("h", "Opening Hand Size")

        elif text.startswith("3"):

            self.create_input("n", "Deck Size")

            self.create_input("a1", "Type 1 Target Cards")
            self.create_input("x1", "Desired Type 1 Targets")

            self.create_input("a2", "Type 2 Target Cards")
            self.create_input("x2", "Desired Type 2 Targets")

            self.create_input("h", "Opening Hand Size")

        elif text.startswith("4"):

            self.create_input("n", "Deck Size")
            self.create_input("a1", "Type 1 Target Cards")
            self.create_input("a2", "Type 2 Target Cards")
            self.create_input("h", "Opening Hand Size")

    # ---------------- CALCULATE ---------------- #

    def calculate(self, instance):

        try:

            mode = self.spinner.text

            result = 0

            description = ""

            # ---------- MODE 1 ---------- #

            if mode.startswith("1"):

                n = int(self.fields["n"].text)
                a = int(self.fields["a"].text)
                x = int(self.fields["x"].text)
                h = int(self.fields["h"].text)

                result = (
                    specific_hand_probability(a, x, n, h)
                    * 100
                )

                description = (
                    f"Exact {x} target cards"
                )

            # ---------- MODE 2 ---------- #

            elif mode.startswith("2"):

                n = int(self.fields["n"].text)
                a = int(self.fields["a"].text)
                h = int(self.fields["h"].text)

                result = (
                    at_least_one_target_probability(a, n, h)
                    * 100
                )

                description = (
                    "At least one target"
                )

            # ---------- MODE 3 ---------- #

            elif mode.startswith("3"):

                n = int(self.fields["n"].text)

                a1 = int(self.fields["a1"].text)
                x1 = int(self.fields["x1"].text)

                a2 = int(self.fields["a2"].text)
                x2 = int(self.fields["x2"].text)

                h = int(self.fields["h"].text)

                result = (
                    dual_target_probability(
                        a1,
                        x1,
                        a2,
                        x2,
                        n,
                        h
                    )
                    * 100
                )

                description = (
                    f"{x1} Type1 and {x2} Type2"
                )

            # ---------- MODE 4 ---------- #

            elif mode.startswith("4"):

                n = int(self.fields["n"].text)

                a1 = int(self.fields["a1"].text)
                a2 = int(self.fields["a2"].text)

                h = int(self.fields["h"].text)

                result = (
                    at_least_one_each_target(
                        a1,
                        a2,
                        n,
                        h
                    )
                    * 100
                )

                description = (
                    "At least one of each"
                )

            else:

                self.result_label.text = "Select a function"
                return

            final_result = round(result, 2)

            self.result_label.text = (
                f"Probability = {final_result}%"
            )

            self.add_history(
                description,
                final_result
            )

        except:

            self.result_label.text = "Invalid Input"

    # ---------------- HISTORY ---------------- #

    def add_history(self, description, result):

        time_now = datetime.now().strftime("%H:%M:%S")

        text = (
            f"[{time_now}] "
            f"{description} --> {result}%"
        )

        label = Label(
            text=text,
            size_hint_y=None,
            height=60,
            font_size=18
        )

        self.history_layout.add_widget(label)

    def clear_history(self, instance):

        self.history_layout.clear_widgets()


# ---------------- RUN ---------------- #

ProbabilityApp().run()
