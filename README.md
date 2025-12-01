# MicroPython Plotter: Quick Start Guide

This library helps you visualize data from your MicroPython device instantly. Follow these steps to get started.

### Installation

Before coding, you need to put the library on your device.

1. Install `mpremote` package in your python environment 

2. Use the `install.sh` or `install.cmd` script 

or:

1. Connect your device to your computer.

2. Open *honny.

3. Upload the `mp_plotter.py` file to the **`lib`** folder on your device.



### How to Use in Code

Using the plotter is very easy. 

1. Import the library in the file you want to use

```
from mp_plotter import plotter
```

2. Call `plotter.plot()` to plot.

Here is a simple example:

```Python
import time
from mp_plotter import plotter  # Import the library

# Main loop
while True:
    value1 = 100
    value2 = 255
    
    # Send data to the plotter
    # You can send between 1 to 5 variables at once
    # in the current version, they should be int and positive
    # such as two int
    plotter.plot(value1, value2)
    
    # maximum 5 variables
    # plotter.plot(value1, value2, value3, value4, value5)
    
    time.sleep(0.05)
```



### Notes

- **Data Types:** You can plot integers (`int`) or decimals (`float`). Note that `float` values are automatically converted to integers before sending. In the future more type will be supported.
- **Limit:** You can plot a maximum of 5 variables at the same time.
- **Visualizing:** Open the micropython-plotter software to see your graphs in real-time using `Plot` tool.



### About `print()`

To make the plotting fast and smooth, this library **disables the standard Python `print()` function** by default. Namely:

- **If you use `print()`:** Nothing will happen.
- **If you need to debug text:** Use `plotter.print("hello")` instead.
- **If you want to enable the original print():** You can manually turn it back on by running `plotter.restore_print()`.