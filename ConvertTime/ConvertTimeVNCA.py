import tkinter as tk
from tkinter import ttk
from datetime import datetime
import pytz


# Function to convert timezones
def convert_timezone():
    # Get the input datetime
    input_datetime_str = entry_datetime.get()
    try:
        # Parse the input datetime
        input_datetime = datetime.strptime(input_datetime_str, '%Y-%m-%d %H:%M:%S')

        # Define timezones
        vn_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
        toronto_timezone = pytz.timezone('America/Toronto')

        # Localize the input datetime to Vietnam timezone
        vn_datetime = vn_timezone.localize(input_datetime)

        # Convert to Toronto timezone
        toronto_datetime = vn_datetime.astimezone(toronto_timezone)

        # Display the result
        result_var.set(toronto_datetime.strftime('%Y-%m-%d %H:%M:%S'))
    except ValueError:
        result_var.set('Invalid datetime format. Use YYYY-MM-DD HH:MM:SS')


# Create the main window
root = tk.Tk()
root.title('Timezone Converter: Vietnam to Toronto')
root.geometry('400x200')

# Create and place widgets
ttk.Label(root, text='Enter datetime (YYYY-MM-DD HH:MM:SS)').pack(pady=10)
entry_datetime = ttk.Entry(root, width=25)
entry_datetime.pack(pady=5)

ttk.Button(root, text='Convert', command=convert_timezone).pack(pady=10)

result_var = tk.StringVar()
ttk.Label(root, textvariable=result_var).pack(pady=10)

# Run the application
root.mainloop()
