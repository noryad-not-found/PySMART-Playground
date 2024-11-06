from pySMART import Device
import subprocess


class PySmartBasic:
    """Class to test features of Pysmart."""

    def __init__(self: str, disk):
        """Declare the device to be checked.

        Args:
            deivce (str): Identifier of the device to
            be checked.
        """

        self.device = Device(disk)

    def check_health(self):
        if self.device.assessment == "PASS":
            print("Drive is healthy!")
        else:
            print("Drive may have issues.")

    def get_attributes(self):
        """Get the attributes of the device."""
        if not self.device.if_attributes: return
        for attribute in self.device.if_attributes:
            print(f"{attribute.name}: {attribute.raw}")

    def get_attributes_value(self, attributes: list = None):
        """Get the attributes of the device.
        Args:
            attributes (list, optional): Optional list with the name of attributes to get.
            Defaults to None.
        """
        if list is None:
            for attribute in self.device.attributes:
                print(f"{attribute.name}: {attribute.raw}")
        else:
            for attribute in self.device.attributes:
                if attribute.name in attributes:
                    print(f"{attribute.name}: {attribute.raw}")
command = "sudo echo YOU NEED SUPERUSER PRIVILEGES"

try:
    # Prompt for sudo password and run command
    subprocess.run(["sudo"] + command.split(), check=True)
except subprocess.CalledProcessError as e:
    print("An error occurred:", e)

test_pysmart = PySmartBasic("nvme0")

test_pysmart.get_attributes()
