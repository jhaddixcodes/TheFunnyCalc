"""
A basic calculator app that always outputs the wrong values (if you consent)
"""

import tkinter as tk
from tkinter import ttk

from equation_parser import evaluate
from utility_functions import uncorrect, custom_round


class Calculator(tk.Frame):
    """
    Main calculator frame
    """

    def __init__(self, parent, *args, **kwargs):
        """
        :param parent: The parent of the frame (should be the root)
        :param args: Other arguments
        :param kwargs: Keyword arguments
        """
        super().__init__(parent, *args, **kwargs)

        # style database manipulator using the clam theme
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # configure styles
        self.style.configure("DisplayStyle.TLabel", relief="flat", background="white", font=("TkFixedFont", 20))
        self.style.configure("ButtonStyle.TButton", foreground="black", background="light blue", font=("TkFixedFont", 20), bordercolor="black")
        self.style.configure("FunnyModeOff.TButton", foreground="black", background="red", font=("TkFixedFont", 20), bordercolor="black")
        self.style.configure("FunnyModeOn.TButton", foreground="black", background="lime", font=("TkFixedFont", 20), bordercolor="black")

        # this ensures the full button won't change color when we hover over it. we do want a relief though
        self.style.map("TButton", background=[], borderwidth=[("active", 1), ("!active", 0), ("pressed", 0)])

        self.expression = tk.StringVar()
        self.funny_mode = tk.BooleanVar()
        self.funny_mode.set(False)
        self.funny_mode_text = tk.StringVar()
        self.funny_mode_text.set("Funny Mode Off")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(3, weight=2)
        self.rowconfigure(4, weight=2)
        self.rowconfigure(5, weight=2)
        self.rowconfigure(6, weight=2)

        self.display = ttk.Label(self, textvariable=self.expression, style="DisplayStyle.TLabel")
        self.display.focus_set()
        self.display.grid(row=0, column=0, columnspan=4, sticky='nsew')
        self.display.bind("<Configure>", self.wrap_update)
        self.display.bind("<Key>", self.handle_key_press)
        self.display.bind("<Return>", lambda event: self.equals())
        self.display.bind("<BackSpace>", lambda event: self.backspace())

        # row 1
        ttk.Button(self, text="C", style="ButtonStyle.TButton", command=self.clear).grid(row=1, column=0, sticky='nsew')
        self.create_character_button("(", row=1, column=1)
        self.create_character_button(")", row=1, column=2)
        self.create_character_button("^", row=1, column=3)

        # row 2
        self.create_character_button("7", row=2, column=0)
        self.create_character_button("8", row=2, column=1)
        self.create_character_button("9", row=2, column=2)
        self.create_character_button("*", row=2, column=3)

        # row 3
        self.create_character_button("4", row=3, column=0)
        self.create_character_button("5", row=3, column=1)
        self.create_character_button("6", row=3, column=2)
        self.create_character_button("/", row=3, column=3)

        # row 4
        self.create_character_button("1", row=4, column=0)
        self.create_character_button("2", row=4, column=1)
        self.create_character_button("3", row=4, column=2)
        self.create_character_button("-", row=4, column=3)

        # row 5
        self.create_character_button("0", row=5, column=0)
        self.create_character_button(".", row=5, column=1)
        ttk.Button(self, text="Del", style="ButtonStyle.TButton", command=self.backspace).grid(row=5, column=2, sticky='nsew')
        self.create_character_button("+", row=5, column=3)

        # row 6
        self.funny_mode_button = ttk.Button(self, textvariable=self.funny_mode_text, style="FunnyModeOff.TButton", command=self.toggle_funny_mode)
        self.funny_mode_button.grid(row=6, column=0, columnspan=2, sticky='nsew')

        ttk.Button(self, text="=", style="ButtonStyle.TButton", command=self.equals).grid(row=6, column=2, columnspan=2, sticky='nsew')

    @staticmethod
    def wrap_update(event):
        """
        Called when window is resized to ensure display text is visible at all times
        :param event: The configure event
        :return:
        """
        ttk.Style().configure(event.widget.winfo_class(), wraplength=(event.widget.winfo_width() - 25))

    def handle_key_press(self, event):
        """
        Called when key is pressed and either runs function or adds character to expression
        :param event: The key event
        :return:
        """
        allowed_keys = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", "*", "/", "^", "(", ")", ".", "=", "c"]
        character = event.char
        if character in allowed_keys:
            if character == "=":
                self.equals()
            elif character == "c":
                self.clear()
            else:
                self.expression.set(self.expression.get() + character)

    def make_character_adder(self, character: str):
        """
        This function creates a character adder function and returns it for use in button commands
        :param character: The character to make a function for
        :return: Character adder function
        """
        def character_adder():
            """
            Concatenates character to the display screen
            :return:
            """
            self.expression.set(self.expression.get() + character)
            self.display.focus_set()
        return character_adder

    def create_character_button(self, character: str, row: int, column: int):
        """
        Creates character button and puts it on the calculator frame
        :param character: Character of the button
        :param row: Row the button is in
        :param column: Column the button is in
        :return:
        """
        ttk.Button(self, text=character, style="ButtonStyle.TButton", command=self.make_character_adder(character)).grid(row=row, column=column, sticky='nsew')

    def backspace(self):
        """
        Removes character from the display screen
        :return:
        """
        self.expression.set(self.expression.get()[:-1])
        self.display.focus_set()

    def clear(self):
        """
        Clears display.
        :return:
        """
        self.expression.set("")
        self.display.focus_set()

    def equals(self):
        """
        Evaluates the current expression in the display screen and prints it on the display.
        :return:
        """
        if not self.funny_mode.get():
            self.expression.set(custom_round(evaluate(self.expression.get())))
        else:
            self.expression.set(custom_round(uncorrect(evaluate(self.expression.get()))))
        self.display.focus_set()

    def toggle_funny_mode(self):
        """
        Toggles funny mode.
        :return:
        """
        self.funny_mode.set(not self.funny_mode.get())
        self.funny_mode_button.configure(style="FunnyModeOn.TButton" if self.funny_mode.get() else "FunnyModeOff.TButton")
        self.funny_mode_text.set("Funny Mode On" if self.funny_mode_text.get() == "Funny Mode Off" else "Funny Mode Off")
        self.display.focus_set()


class Application(tk.Tk):
    """
    The main Tk application.
    """
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.title("The Fucked Up Calculator")
        self.geometry("450x600")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        Calculator(self).grid(row=0, column=0, sticky="NSEW")


if __name__ == '__main__':
    app = Application()
    app.mainloop()
