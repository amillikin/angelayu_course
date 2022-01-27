from tkinter import *

def convert():
    converted_km = float(miles.get()) * 1.609
    label_km_val.config(text=f"{converted_km}")

window = Tk()
window.title("Miles to Kilometer Converter")
window.config(padx=20, pady=20)

miles = IntVar()
entry_miles = Entry(width=5, textvariable=miles)
entry_miles.grid(row=0, column=1)

label_miles = Label(text="Miles")
label_miles.grid(row=0, column=2)

label_equals = Label(text="is equal to")
label_equals.grid(row=1, column=0)

label_km_val = Label(text="0")
label_km_val.grid(row=1, column=1)

label_km = Label(text="Km")
label_km.grid(row=1, column=2)

button_calc = Button(text="Calculate", command=convert)
button_calc.grid(row=2, column=1)

window.mainloop()
