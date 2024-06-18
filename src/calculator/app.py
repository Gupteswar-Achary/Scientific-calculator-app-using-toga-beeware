import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import math
import cmath


class CalculatorApp(toga.App):
    def startup(self):
        self.main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        self.result = toga.TextInput(readonly=True, style=Pack(flex=1, padding_bottom=10))
        self.main_box.add(self.result)

        self.button_layout = [
            ('DEL', '√', '^', 'Sci'),
            ('1', '2', '3', '+'),
            ('4', '5', '6', '-'),
            ('7', '8', '9', '*'),
            ('.', '0', 'C', '=')
        ]

        self.create_buttons(self.button_layout, self.main_box)

        self.scientific_mode_layout = [
            ('', 'Math', ''),
            ('', 'Cubic', 'Quad', '')
        ]

        self.sci_box = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=1))
        self.sci_result = toga.TextInput(readonly=True, style=Pack(flex=1, padding_bottom=10))
        self.sci_box.add(self.sci_result)
        self.create_buttons(self.scientific_mode_layout, self.sci_box)

        self.quadratic_layout = [
            ('a', toga.TextInput(style=Pack(flex=1))),
            ('b', toga.TextInput(style=Pack(flex=1))),
            ('c', toga.TextInput(style=Pack(flex=1))),
            ('Solve Quad', None)
        ]

        self.quad_box = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=1))
        self.quad_result = toga.TextInput(readonly=True, style=Pack(flex=1, padding_bottom=10))
        self.quad_box.add(self.quad_result)
        self.create_equation_solver_ui(self.quadratic_layout, self.quad_box, self.on_solve_quadratic)

        self.cubic_layout = [
            ('a', toga.TextInput(style=Pack(flex=1))),
            ('b', toga.TextInput(style=Pack(flex=1))),
            ('c', toga.TextInput(style=Pack(flex=1))),
            ('d', toga.TextInput(style=Pack(flex=1))),
            ('Solve Cubic', None)
        ]

        self.cubic_box = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=1))
        self.cubic_result = toga.TextInput(readonly=True, style=Pack(flex=1, padding_bottom=10))
        self.cubic_box.add(self.cubic_result)
        self.create_equation_solver_ui(self.cubic_layout, self.cubic_box, self.on_solve_cubic)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()

    def create_buttons(self, layout, container):
        for row in layout:
            button_box = toga.Box(style=Pack(direction=ROW, padding_bottom=5))
            for text in row:
                if text:
                    button = toga.Button(text, on_press=self.on_button_press, style=Pack(flex=1, padding=5))
                    button_box.add(button)
            container.add(button_box)

    def create_equation_solver_ui(self, layout, container, solve_method):
        for label_text, widget in layout:
            box = toga.Box(style=Pack(direction=ROW, padding_bottom=5))
            label = toga.Label(label_text, style=Pack(padding=5))
            box.add(label)
            if widget:  # Check if widget is not None
                box.add(widget)
            container.add(box)

        solve_button = toga.Button('Solve', on_press=solve_method, style=Pack(padding=10))
        container.add(solve_button)
        back_button = toga.Button('Math', on_press=self.show_main_calculator, style=Pack(padding=10))
        container.add(back_button)

    def on_button_press(self, widget):
        if widget.text == 'DEL':
            self.result.value = self.result.value[:-1]
        elif widget.text == '√':
            try:
                self.result.value = str(math.sqrt(float(self.result.value)))
            except ValueError:
                self.result.value = "Error"
        elif widget.text == '^':
            self.result.value += widget.text
        elif widget.text == 'Sci':
            self.main_window.content = self.sci_box
        elif widget.text == 'Math':
            self.main_window.content = self.main_box
        elif widget.text == 'C':
            self.result.value = ''
        elif widget.text == '=':
            if "^" in self.result.value:
                self.calculate_power()
            else:
                self.calculate()
        elif widget.text == 'Quad':
            self.main_window.content = self.quad_box
        elif widget.text == 'Cubic':
            self.main_window.content = self.cubic_box
        else:
            self.result.value += widget.text

    def show_main_calculator(self, widget):
        self.main_window.content = self.main_box

    def calculate(self):
        try:
            self.result.value = str(eval(self.result.value))
        except Exception:
            self.result.value = "Error"

    def calculate_power(self):
        try:
            base, exponent = self.result.value.split('^')
            number = float(base)
            power_value = float(exponent)
            self.result.value = str(pow(number, power_value))
        except ValueError:
            self.result.value = "Error"

    def on_solve_quadratic(self, widget):
        try:
            a = float(self.quadratic_layout[0][1].value)
            b = float(self.quadratic_layout[1][1].value)
            c = float(self.quadratic_layout[2][1].value)
            d = b ** 2 - 4 * a * c  # discriminant

            if d >= 0:
                root1 = (-b + math.sqrt(d)) / (2 * a)
                root2 = (-b - math.sqrt(d)) / (2 * a)
            else:
                root1 = (-b + cmath.sqrt(d)) / (2 * a)
                root2 = (-b - cmath.sqrt(d)) / (2 * a)

            self.quad_result.value = f'Roots: {root1}, {root2}'
        except ValueError:
            self.quad_result.value = "Error"

    def on_solve_cubic(self, widget):
        try:
            a = float(self.cubic_layout[0][1].value)
            b = float(self.cubic_layout[1][1].value)
            c = float(self.cubic_layout[2][1].value)
            d = float(self.cubic_layout[3][1].value)
            f = ((3 * c / a) - (b ** 2 / a ** 2)) / 3
            g = ((2 * b ** 3 / a ** 3) - (9 * b * c / a ** 2) + (27 * d / a)) / 27
            h = (g ** 2) / 4 + (f ** 3) / 27

            if h > 0:
                r = -(g / 2) + math.sqrt(h)
                s = r ** (1 / 3)
                t = -(g / 2) - math.sqrt(h)
                u = (t ** (1 / 3))
                root1 = (s + u) - (b / (3 * a))
                self.cubic_result.value = f'Root: {root1}'
            elif f == 0 and g == 0 and h == 0:
                root1 = -((d / a) ** (1 / 3))
                self.cubic_result.value = f'Root: {root1}'
            else:
                i = math.sqrt(((g ** 2) / 4) - h)
                j = i ** (1 / 3)
                k = math.acos(-(g / (2 * i)))
                l = -j
                m = math.cos(k / 3)
                n = math.sqrt(3) * math.sin(k / 3)
                p = -(b / (3 * a))

                root1 = 2 * j * math.cos(k / 3) - (b / (3 * a))
                root2 = l * (m + n) + p
                root3 = l * (m - n) + p
                self.cubic_result.value = f'Roots: {root1}, {root2}, {root3}'
        except ValueError:
            self.cubic_result.value = "Error"


def main():
    return CalculatorApp('Calculator', 'org.beeware.calculator')


if __name__ == '__main__':
    main().main_loop()
