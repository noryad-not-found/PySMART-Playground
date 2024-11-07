import json
import matplotlib.pyplot as plt
from pySMART import Device, DeviceList, SMARTCTL
from datetime import datetime


class PySmartBasicPlotter:
    """Class to test features of PySMART for managing and checking SMART attributes of devices."""

    def __init__(self, disks: list = None):
        """Initialize with a list of disks or load all available devices.

        Args:
            disks (list, optional): List of device identifiers to check.
        """
        SMARTCTL.sudo = True  # Ensure SMARTCTL runs with sudo permissions
        self.devices = (
            [Device(disk) for disk in disks] if disks else DeviceList().devices
        )

    def check_health(self):
        """Check and print the health status of each device."""
        for device in self.devices:
            if device.assessment == "PASS":
                print(f"Drive {device.name} is healthy!")
            else:
                print(f"Drive {device.name} may have issues.")

    def get_attributes(self, attributes_list: list = None):
        """Collect SMART attributes for each device."""
        attributes_data = {}
        for device in self.devices:
            attributes = getattr(device, "if_attributes", None)
            if attributes is None:
                print(f"No SMART attributes found for device {device.name}.")
                continue
            
            # Collect attributes to a dictionary for this device
            device_data = {}
            
            for key, value in attributes.__dict__.items():
                if attributes_list and key not in attributes_list:
                    continue
                try:
                    device_data[key] = str(value) if value is not None else 'None'
                except Exception as e:
                    device_data[key] = len(value)
                    print(f"Error processing attribute {key}: {e}")
                    device_data[key] = 'None'
            
            attributes_data[device.name] = device_data

        return attributes_data

    def save_attributes_to_json(self, filename=str(datetime.now().date()) + "_smart_attributes.json"):
        """Save SMART attributes to a JSON file."""
        attributes_data = self.get_attributes()
        with open(filename, "w") as json_file:
            json.dump(attributes_data, json_file, indent=4)
        print(f"SMART attributes saved to {filename}")


    def plot_attributes(self, attributes_data, large_value_threshold=1000):
        """Plot SMART attributes from the data dictionary, grouped by categories and large values separately."""
        
        for device_name, attributes in attributes_data.items():
            # Convert values to integers if possible, or set to 0 if not
            numeric_attributes = {k: int(v) if str(v).isdigit() else 0 for k, v in attributes.items()}

            # Group attributes
            power_metrics = {k: v for k, v in numeric_attributes.items() if "power" in k.lower()}
            temperature_metrics = {k: v for k, v in numeric_attributes.items() if "temperature" in k.lower()}
            error_metrics = {k: v for k, v in numeric_attributes.items() if "error" in k.lower() or "warning" in k.lower()}
            data_transfer_metrics = {k: v for k, v in numeric_attributes.items() if "bytesread" in k.lower() or "byteswritten" in k.lower()}
            
            # Separate large values (above threshold) from smaller ones
            large_metrics = {k: v for k, v in numeric_attributes.items() if v >= large_value_threshold}
            small_metrics = {
                k: v for k, v in numeric_attributes.items()
                if k not in large_metrics and k not in power_metrics and k not in temperature_metrics and k not in error_metrics and k not in data_transfer_metrics
            }

            # Function to create a bar plot for a given dictionary of attributes
            def plot_bar_chart(metrics, title):
                if not metrics:
                    return
                attribute_names = list(metrics.keys())
                attribute_values = list(metrics.values())

                plt.figure(figsize=(10, 5))
                plt.bar(attribute_names, attribute_values, color="skyblue")
                plt.xlabel("Attributes")
                plt.ylabel("Values")
                plt.title(f"{title} for {device_name}")
                plt.xticks(rotation=45, ha="right")
                plt.tight_layout()
                plt.show()

            # Plot each group separately
            plot_bar_chart(power_metrics, "Power Metrics")
            plot_bar_chart(temperature_metrics, "Temperature and Time Metrics")
            plot_bar_chart(error_metrics, "Error and Warning Metrics")
            plot_bar_chart(data_transfer_metrics, "Data Transfer Metrics (Bytes Read/Written)")
            plot_bar_chart(small_metrics, "Other Small Metrics")
            plot_bar_chart(large_metrics, "Large Metrics (Values ≥ Threshold)")

            
    @staticmethod
    def load_and_plot_from_json(filename="smart_attributes.json"):
        """Load SMART attributes from a JSON file and plot them."""
        with open(filename, "r") as json_file:
            attributes_data = json.load(json_file)

        plotter = PySmartBasicPlotter()
        plotter.plot_attributes(attributes_data)