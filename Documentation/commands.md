# Commands #

Basic commands to interact with the disks using `smartctl`.

- **Lists all disks**:

    ```bash
    smartctl --scan
    ```

    Output:

    ```bash
    /dev/nvme0 -d nvme # /dev/nvme0, NVMe device
    ```

- **View General Disk Info**:

    ```bash
    smartctl -i /dev/sdX
    ```
    Output:

    ```bash
    Copyright (C) 2002-23, Bruce Allen, Christian Franke, www.smartmontools.org

    === START OF INFORMATION SECTION ===
    Model Number:                       WD PC SN740 SDDQMQD-512G-1201
    Serial Number:                      233464800867
    Firmware Version:                   73116101
    PCI Vendor/Subsystem ID:            0x15b7
    IEEE OUI Identifier:                0x001b44
    Total NVM Capacity:                 512,110,190,592 [512 GB]
    Unallocated NVM Capacity:           0
    Controller ID:                      0
    NVMe Version:                       1.4
    Number of Namespaces:               1
    Namespace 1 Size/Capacity:          512,110,190,592 [512 GB]
    Namespace 1 Formatted LBA Size:     512
    Namespace 1 IEEE EUI-64:            001b44 8b4a3c7cbe
    Local Time is:                      Wed Nov  6 13:06:47 2024 CET


    ```

- **Check Disk Health Status**:

    ```bash
    smartctl -H /dev/sdX
    ```
    Output:

    ```bash
    smartctl 7.4 2023-08-01 r5530 [x86_64-linux-6.8.0-48-generic] (local build)
    Copyright (C) 2002-23, Bruce Allen, Christian Franke, www.smartmontools.org

    === START OF SMART DATA SECTION ===
    SMART overall-health self-assessment test result: PASSED

    ```

- **View All S.M.A.R.T. Attributes**:

    ```bash
    smartctl -A /dev/sdX
    ```

    Output:

    ```bash
    smartctl 7.4 2023-08-01 r5530 [x86_64-linux-6.8.0-48-generic] (local build)
    Copyright (C) 2002-23, Bruce Allen, Christian Franke, www.smartmontools.org

    === START OF SMART DATA SECTION ===
    SMART/Health Information (NVMe Log 0x02)
    Critical Warning:                   0x00
    Temperature:                        48 Celsius
    Available Spare:                    100%
    Available Spare Threshold:          10%
    Percentage Used:                    0%
    Data Units Read:                    4,382,651 [2.24 TB]
    Data Units Written:                 4,002,344 [2.04 TB]
    Host Read Commands:                 23,800,693
    Host Write Commands:                96,773,152
    Controller Busy Time:               83
    Power Cycles:                       64
    Power On Hours:                     73
    Unsafe Shutdowns:                   21
    Media and Data Integrity Errors:    0
    Error Information Log Entries:      0
    Warning  Comp. Temperature Time:    0
    Critical Comp. Temperature Time:    0
    Temperature Sensor 1:               57 Celsius
    Temperature Sensor 2:               48 Celsius
    ```

- **Run Self-Tests**:
  - Short test: `smartctl -t short /dev/sdX`
  - Long test: `smartctl -t long /dev/sdX`
