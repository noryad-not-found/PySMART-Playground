import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import subprocess
import matplotlib.pyplot as plt
import re


class DiskInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disk Information Lookup")
        self.root.geometry("900x800")

        # Set up the GUI components
        self.label = tk.Label(self.root, text="Select a disk to get information:", font=("Arial", 14))
        self.label.pack(pady=10)

        # Get available disks and populate the dropdown
        self.disks = self.get_available_disks()

        # Create a ComboBox (dropdown) for disk selection
        self.disk_combobox = ttk.Combobox(self.root, values=self.disks, width=40)
        self.disk_combobox.pack(pady=10)

        # Button to fetch disk information
        self.info_button = tk.Button(self.root, text="Get Disk Info", command=self.show_disk_info, font=("Arial", 12))
        self.info_button.pack(pady=10)

        # Canvas for matplotlib chart
        self.chart_canvas = tk.Canvas(self.root, width=500, height=300)
        self.chart_canvas.pack(pady=10)

    def run_command(self, command):
        """Runs a system command and returns the output."""
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return result.decode('utf-8')
        except subprocess.CalledProcessError as e:
            return f"Error: {e.output.decode('utf-8')}"

    def get_available_disks(self):
        """Gets available disks using lsblk and returns them as a list."""
        command = "lsblk -o NAME,TYPE | grep disk"  # List devices of type 'disk'
        output = self.run_command(command)
        disks = []
        
        # Process the output to get disk names
        for line in output.splitlines():
            disk_info = line.split()
            if len(disk_info) >= 2 and disk_info[1] == "disk":
                disks.append(f"/dev/{disk_info[0]}")
        
        return disks

    def get_device_type(self, disk_name):
        """Determine the type of disk (e.g., NVMe, SATA, USB)"""
        if "nvme" in disk_name.lower():
            return "nvme"
        elif "sd" in disk_name.lower():
            return "sata"
        elif "usb" in disk_name.lower():
            return "usb"
        else:
            return "unknown"

    def get_disk_info(self, disk_name):
        """Gets detailed information about the selected disk using smartctl."""
        device_type = self.get_device_type(disk_name)

        if device_type == "nvme":
            command = f"sudo smartctl -a -d nvme {disk_name}"
        elif device_type == "usb":
            command = f"sudo smartctl -a -d sat {disk_name}"
        elif device_type == "sata":
            command = f"sudo smartctl -a {disk_name}"
        else:
            return f"Error: Unable to determine device type for {disk_name}"

        output = self.run_command(command)
        return output

    def parse_smartctl_output(self, output):
        """Parses smartctl output to extract specific information for plotting."""
        parsed_data = {
            'Temperature': None,
            'Power_On_Hours': None,
            'Unsafe_Shutdowns': None,
            'Health': 'Unknown'
        }

        # Search for specific patterns in the output
        temperature_match = re.search(r"Temperature:\s+(\d+)\s+Celsius", output)
        power_on_match = re.search(r"Power On Hours:\s+(\d+)\s", output)
        reallocated_match = re.search(r"Unsafe Shutdowns:\s+(\d+)\s", output)
        health_match = re.search(r"(SMART overall-health self-assessment test result): (\w+)", output)

        if temperature_match:
            parsed_data['Temperature'] = int(temperature_match.group(1))
        if power_on_match:
            parsed_data['Power_On_Hours'] = int(power_on_match.group(1))
        if reallocated_match:
            parsed_data['Unsafe_Shutdowns'] = int(reallocated_match.group(1))
        if health_match:
            parsed_data['Health'] = health_match.group(2)

        return parsed_data

    def show_disk_info(self):
        """Fetches, parses, and displays the information for the selected disk."""
        selected_disk = self.disk_combobox.get()
        
        if not selected_disk:
            messagebox.showerror("Error", "Please select a disk.")
            return

        # Fetch disk information
        disk_info = self.get_disk_info(selected_disk)
        parsed_data = self.parse_smartctl_output(disk_info)

        # Clear any existing chart
        for widget in self.chart_canvas.winfo_children():
            widget.destroy()

        # Create and display a chart with the parsed data
        self.display_chart(parsed_data)

    def display_chart(self, parsed_data):
        """Displays a chart of parsed data using matplotlib."""
        fig, ax = plt.subplots(figsize=(5, 3))

        # Bar chart data
        labels = ['Temperature', 'Power On Hours', 'Reallocated Sectors']
        values = [
            parsed_data.get('Temperature', 0),
            parsed_data.get('Power_On_Hours', 0),
            parsed_data.get('Unsafe_Shutdowns', 0)
        ]

        ax.bar(labels, values, color=['#FF9999', '#66B3FF', '#99FF99'])
        ax.set_title(f"Disk Health: {parsed_data['Health']}")
        ax.set_ylabel("Value")
        ax.set_xlabel("Attributes")

        # Embedding the plot in the Tkinter canvas
        chart = FigureCanvasTkAgg(fig, master=self.chart_canvas)
        chart.draw()
        chart.get_tk_widget().pack()


# Main function to run the app
def main():
    root = tk.Tk()
    app = DiskInfoApp(root)
    root.mainloop()


# Run the app
if __name__ == "__main__":
    main()