import customtkinter
from typing import Union, Callable

class FloatSpinbox(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
                 text: str = '',
                 default_val: float = 0.0,
                 min: float = - 10**9,
                 max: float = 10**9,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.min = min
        self.max = max
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.has_label = (text != '')

        if self.has_label:
            self.label = customtkinter.CTkLabel(self, text=text)
            self.label.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.subtract_button = customtkinter.CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=1, padx=(3, 0), pady=3)

        self.entry = customtkinter.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0)
        self.entry.grid(row=0, column=2, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = customtkinter.CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=3, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, str(default_val))

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) + self.step_size
            if (value >= self.min) and (value <= self.max):
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
            else:
                if (value <= self.min):
                    self.entry.delete(0, "end")
                    self.entry.insert(0, self.min)
                if (value >= self.max):
                    self.entry.delete(0, "end")
                    self.entry.insert(0, self.max)                
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) - self.step_size
            if (value >= self.min) and (value <= self.max):
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> Union[float, None]:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        if (value >= self.min) and (value <= self.max):
            self.entry.delete(0, "end")
            self.entry.insert(0, str(float(value)))
        else:
            raise ValueError(f'the value {value} is not in the range [{self.min},{self.max}]')