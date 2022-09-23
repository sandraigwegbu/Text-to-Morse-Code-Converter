# TEXT TO MORSE CODE CONVERTER
from chars import characters
from tkinter import *
from tkinter import messagebox
import winsound
import time
import threading
import os


# ------------------------------------------ TEXT to MORSE CODE CONVERSION ------------------------------------------ #
converted_text = None  # global variable


def convert_text():
	global converted_text

	text = text_entry.get().lower()

	valid_entry = False
	for char in text:
		try:
			converted_text = "     ".join([characters[char] for char in text])
		except KeyError:
			messagebox.showerror(title="Oops!", message="Please type message containing only:\n\nA-Z, 0-9 and spaces.")
			break
		else:
			morse_code.config(text=converted_text)
			valid_entry = True

	if valid_entry is True:
		thread = threading.Thread(target=generate_beeps)
		thread.start()


# -------------------------------------------------- BEEP GENERATOR ------------------------------------------------- #
def generate_beeps():
	global converted_text

	dot_duration = 200  # milliseconds
	dash_duration = 1000  # milliseconds
	frequency = 500  # Hz

	if converted_text is not None:
		submit.config(state="disabled", text="Wait...")

		for char in converted_text:
			if char == ".":
				winsound.Beep(frequency, dot_duration)  # dot
			elif char == "–":
				winsound.Beep(frequency, dash_duration)  # dash
			elif char == " ":
				time.sleep(0.2)

		# Reset window
		time.sleep(1)
		text_entry.delete(0, END)  # clears entry box
		morse_code.config(text="Morse Code Converter")
		submit.config(state="normal", text="Convert")


# ---------------------------------------- CLOSE WINDOW & TERMINATE PROGRAM ----------------------------------------- #
def on_closing():
	if messagebox.askokcancel("Quit", "Do you want to quit?"):
		window.destroy()  # closes window
		os._exit(0)       # stops script


# ---------------------------------------------------- UI SETUP ----------------------------------------------------- #
# CONSTANTS
BACKGROUND = "#F9F5EB"
TEXT_COLOUR = "#1C3879"
ACCENT_COLOUR = "#607EAA"
BUTTON1_COLOUR = "#EAE3D2"
BUTTON2_COLOUR = '#FFFFFF'


# WINDOW CONFIGURATION
window = Tk()
window.title("Text to Morse Code Converter")
window.minsize(700, 400)
window.config(padx=50, pady=50, bg=BACKGROUND)

for num in range(0, 4):
	window.columnconfigure(num, weight=1)
	window.rowconfigure(num, weight=1)

# LABEL WIDGETS
morse_code = Label(text="Morse Code Converter", font=("Arial Narrow", 70, "bold"), fg=TEXT_COLOUR, bg=BACKGROUND)
morse_code.config(wraplength=600)
morse_code.grid(column=0, row=0, columnspan=4, rowspan=3)

your_message = Label(text="  Your message:  ", font=("Helvetica", 12), fg=BACKGROUND, bg=ACCENT_COLOUR)
your_message.grid(column=0, row=3, sticky="w")

# ENTRY WIDGET
text_entry = Entry()
text_entry.focus()
text_entry.config(width=44, font=("Helvetica", 11), highlightthickness=10, highlightcolor=BACKGROUND,
                  highlightbackground=BACKGROUND)
text_entry.grid(column=1, row=3, sticky="w")

# BUTTON WIDGET
submit = Button()
submit.config(text="Convert", command=convert_text, state="normal", padx=22, font=("Arial Narrow", 11), fg=TEXT_COLOUR,
              bg=BUTTON1_COLOUR)
submit.grid(column=3, row=3, sticky="e")

# MAINLOOP
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
