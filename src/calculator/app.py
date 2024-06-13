import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import math

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
            try:
                self.result.value = str(float(self.result.value) ** 2)
            except ValueError:
                self.result.value = "Error"
        elif widget.text == 'Sci':
            self.open_sci_window()
        elif widget.text == 'C':
            self.result.value = ''
        elif widget.text == '=':
            self.calculate()
        else:
            self.result.value += widget.text

    def calculate(self):
        try:
            self.result.value = str(eval(self.result.value))
        except Exception:
            self.result.value = "Error"

    def open_sci_window(self):
        sci_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        label = toga.Label('Scientific Mode', style=Pack(padding_bottom=10))
        sci_box.add(label)

        close_button = toga.Button('Close', on_press=self.close_sci_window, style=Pack(padding=10))
        sci_box.add(close_button)

        self.sci_window = toga.Window(title='Scientific Mode')
        self.sci_window.content = sci_box
        self.sci_window.show()

    def close_sci_window(self, widget):
        self.sci_window.close()

def main():
    return CalculatorApp('Calculator', 'org.beeware.calculator')

if __name__ == '__main__':
    main().main_loop()
