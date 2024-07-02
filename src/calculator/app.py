import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import math
import cmath


class CalculatorApp(toga.App):
    def startup(self):
        # creating the main box
        self.main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        self.result = toga.TextInput(readonly=False, style=Pack(flex=1, padding_bottom=10))
        self.main_box.add(self.result)

        self.button_layout = [
            ('AC', 'DEL', 'Tri', 'Equ'),
            ('√', '^', 'ln', '/'),
            ('1', '2', '3', '+'),
            ('4', '5', '6', '-'),
            ('7', '8', '9', '*'),
            ('.', '0', '00', '=')
        ]

        self.create_buttons(self.button_layout, self.main_box)

        # creating the scientific mode UI
        self.scientific_mode_layout = [
            ('Math', 'Tri'),
            ('', 'Cubic', 'Quad', '')
        ]

        self.equ_box = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=1))
        self.equ_result = toga.TextInput(readonly=True, style=Pack(flex=1, padding_bottom=10))
        self.equ_box.add(self.equ_result)
        self.create_buttons(self.scientific_mode_layout, self.equ_box)

        # creating ui for the quadratic equations
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

        # creating ui for the cubic equations
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

        # Creating the Trigonometry box UI
        self.trigonometry_box = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=1))
        self.tri_result = toga.TextInput(readonly=True, style=Pack(flex=1, padding_bottom=10))
        self.trigonometry_box.add(self.tri_result)

        self.trigonometry_layout = [
            ('(', ')', '', 'Math'),
            ('sin', 'cos', 'tan', ''),
            ('cosec', 'sec', 'cot', '')
        ]

        # Adding main calculator buttons to the trigonometry box
        self.create_buttons(self.button_layout, self.trigonometry_box)
        # Adding trigonometry buttons to the trigonometry box
        self.create_buttons(self.trigonometry_layout, self.trigonometry_box)

        self.current_box = self.main_box  # Track the currently active box

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()

    # Creating the buttons layout of math calculator
    def create_buttons(self, layout, container):
        for row in layout:
            button_box = toga.Box(style=Pack(direction=ROW, padding_bottom=5))
            for text in row:
                if text:
                    bg_color = "#3A4452" if text.isdigit() or text == '.' or text in ['sin', 'cos', 'tan', 'cosec', 'sec', 'cot', '(',')'] else "#6DEE6D"
                    color = "#FFFFFF" if text.isdigit() or text == '.' or text in ['sin', 'cos', 'tan', 'cosec', 'sec', 'cot', '(',')'] else "#000000"
                    button = toga.Button(text, on_press=self.on_button_press, style=Pack(flex=1, padding=5, background_color=bg_color, color=color))
                    if text == '=' or text == 'AC' or text == 'DEL':
                        button.style.background_color = "#FFA500"
                    button_box.add(button)
            container.add(button_box)

    # create the button layout of equation mode
    def create_equation_solver_ui(self, layout, container, solve_method):
        for label_text, widget in layout:
            box = toga.Box(style=Pack(direction=ROW, padding_bottom=5))
            label = toga.Label(label_text, style=Pack(padding=5))
            box.add(label)
            if widget:  # Check if widget is not None
                box.add(widget)
            container.add(box)

        solve_button = toga.Button('Solve', on_press=solve_method, style=Pack(padding=10, background_color="#6DEE6D"))
        container.add(solve_button)
        back_button = toga.Button('Math', on_press=self.show_main_calculator, style=Pack(padding=10, background_color="#6DEE6D"))
        container.add(back_button)

    # Function to operate on clicks
    def on_button_press(self, widget):
        if self.current_box == self.trigonometry_box:
            result_box = self.tri_result
        else:
            result_box = self.result

        if widget.text == 'DEL':
            result_box.value = result_box.value[:-1]
        elif widget.text == '√':
            try:
                result_box.value = str(math.sqrt(float(result_box.value)))
            except ValueError:
                result_box.value = "Error"
        elif widget.text == '^':
            result_box.value += widget.text
        elif widget.text == 'Equ':
            self.main_window.content = self.equ_box
            self.current_box = self.equ_box
        elif widget.text == 'Tri':
            self.main_window.content = self.trigonometry_box
            self.current_box = self.trigonometry_box
        elif widget.text == 'Math':
            self.main_window.content = self.main_box
            self.current_box = self.main_box
        elif widget.text == 'AC':
            result_box.value = ''
        elif widget.text == 'ln':
            self.calculate_ln(result_box)
        elif widget.text == '=':
            if "^" in result_box.value:
                self.calculate_power(result_box)
            elif any(func in result_box.value for func in ['sin', 'cos', 'tan', 'cosec', 'sec', 'cot']):
                self.calculate_trigonometry(result_box)
            else:
                self.calculate(result_box)
        elif widget.text == 'Quad':
            self.main_window.content = self.quad_box
            self.current_box = self.quad_box
        elif widget.text == 'Cubic':
            self.main_window.content = self.cubic_box
            self.current_box = self.cubic_box
        else:
            result_box.value += widget.text

    def show_main_calculator(self, widget):
        self.main_window.content = self.main_box
        self.current_box = self.main_box

    # calculate function for simple math functions
    def calculate(self, result_box):
        try:
            result_box.value = str(eval(result_box.value))
        except Exception:
            result_box.value = "Error"

    # function to calculate the power of number
    def calculate_power(self, result_box):
        try:
            base, exponent = result_box.value.split('^')
            number = float(base)
            power_value = float(exponent)
            result_box.value = str(pow(number, power_value))
        except ValueError:
            result_box.value = "Error"

    # function to calculate the natural logarithm
    def calculate_ln(self, result_box):
        try:
            number = float(result_box.value)
            if number > 0:
                result_box.value = str(math.log(number))
            else:
                result_box.value = "Error"
        except ValueError:
            result_box.value = "Error"

    # Function to calculate trigonometric functions
    def calculate_trigonometry(self, result_box):
        try:
            for func in ['sin', 'cos', 'tan', 'cosec', 'sec', 'cot']:
                if func in result_box.value:
                    value = float(result_box.value.replace(f'{func}(', '').replace(')', ''))
                    if func == 'sin':
                        result = math.sin(math.radians(value))
                    elif func == 'cos':
                        result = math.cos(math.radians(value))
                    elif func == 'tan':
                        result = math.tan(math.radians(value))
                    elif func == 'cosec':
                        result = 1 / math.sin(math.radians(value))
                    elif func == 'sec':
                        result = 1 / math.cos(math.radians(value))
                    elif func == 'cot':
                        result = 1 / math.tan(math.radians(value))
                    result_box.value = str(result)
                    return
        except ValueError:
            result_box.value = "Error"

    # Function to calculate quadratic equations
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

    # function to solve the cubic equations
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
