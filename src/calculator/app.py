import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import math
import string

class CalculatorApp(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        self.result = toga.TextInput(readonly=True, style=Pack(flex=1, padding_bottom=10))

        button_layout = [
            ('DEL', '√', '^', 'Sci'),
            ('1', '2', '3', '+'),
            ('4', '5', '6', '-'),
            ('7', '8', '9', '*'),
            ('.', '0', 'C', '=')
        ]

        main_box.add(self.result)
        for row in button_layout:
            button_box = toga.Box(style=Pack(direction=ROW, padding_bottom=5))
            for text in row:
                button = toga.Button(text, on_press=self.on_button_press, style=Pack(flex=1, padding=5))
                button_box.add(button)
            main_box.add(button_box)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

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
            self.open_sci_window()
        elif widget.text == 'Math':
            self.sci_window.close()
        elif widget.text == 'C':
            self.result.value = ''
        elif widget.text == '=':
            if "^" in widget.text:
                self.calculate_power()
            else:
                self.calculate()
        else:
            self.result.value += widget.text



    def open_sci_window(self):

        sci_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        label = toga.Label('Scientific Mode', style=Pack(padding_bottom=10))
        sci_box.add(label)

        self.result = toga.TextInput(readonly=True, style=Pack(flex=1))
        sci_box.add(self.result)

        self.sci_window = toga.Window(title='Scientific Mode')

        button_layout = [
            ('DEL', '√', '^', 'Math'),
            ('1', '2', '3', '+'),
            ('4', '5', '6', '-'),
            ('7', '8', '9', '*'),
            ('.', '0', 'C', '=')
        ]

        for row in button_layout:
            button_box = toga.Box(style=Pack(direction=ROW, padding_bottom=5))
            for text in row:
                button = toga.Button(text, on_press=self.on_button_press, style=Pack(flex=1, padding=5))
                button_box.add(button)
            sci_box.add(button_box)

        self.sci_window.content = sci_box
        self.sci_window.show()

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




def main():
    return CalculatorApp('Calculator', 'org.beeware.calculator')

if __name__ == '__main__':
    main().main_loop()
