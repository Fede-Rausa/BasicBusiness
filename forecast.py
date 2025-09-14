import tkinter as tk
import pandas as pd
import numpy as np
import datetime as dt
import os


class ForecastSales():
    def __init__(self, parent, root):
        self.parent = parent
        self.root = root
        self.root.title("Forecast Sales tool")