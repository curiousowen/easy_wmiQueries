import re

def validate_input(input_str, pattern, example):
    """
    Validate user input against a regex pattern.
    
    Args:
    input_str (str): The user input string.
    pattern (str): The regex pattern to validate against.
    example (str): An example of the expected input.
    
    Returns:
    bool: True if the input is valid, False otherwise.
    """
    if not re.match(pattern, input_str):
        print(f"Invalid input: '{input_str}'. Expected format: {example}")
        return False
    return True

def get_user_input(prompt, pattern, example):
    """
    Prompt the user for input and validate it.
    
    Args:
    prompt (str): The message to display to the user.
    pattern (str): The regex pattern to validate input against.
    example (str): An example of the expected input.
    
    Returns:
    str: The validated user input.
    """
    while True:
        user_input = input(prompt)
        if validate_input(user_input, pattern, example):
            return user_input

def create_wmi_query(category, option, value):
    """
    Create a WMI query based on user-selected category, option, and value.
    
    Args:
    category (str): The selected category.
    option (str): The selected option.
    value (str): The user-provided value for the query.
    
    Returns:
    str: The generated WMI query.
    """
    queries = {
        'Operating System Information': {
            'Version': f"SELECT * FROM Win32_OperatingSystem WHERE Version LIKE '{value}'",
            'Service Pack Level': f"SELECT * FROM Win32_OperatingSystem WHERE ServicePackMajorVersion = {value}"
        },
        'Hardware Information': {
            'Manufacturer': f"SELECT * FROM Win32_ComputerSystem WHERE Manufacturer = '{value}'",
            'Model': f"SELECT * FROM Win32_ComputerSystem WHERE Model = '{value}'",
            'Memory': f"SELECT * FROM Win32_ComputerSystem WHERE TotalPhysicalMemory >= {value}"
        },
        'Disk Space': {
            'Free Space on Logical Disks': f"SELECT * FROM Win32_LogicalDisk WHERE DeviceID = '{value.split()[0]}' AND FreeSpace > {value.split()[1]}"
        },
        'Network Configuration': {
            'IP Address': f"SELECT * FROM Win32_NetworkAdapterConfiguration WHERE IPAddress LIKE '{value}'",
            'DHCP Status': f"SELECT * FROM Win32_NetworkAdapterConfiguration WHERE DHCPEnabled = {value}"
        },
        'System Roles': {
            'Domain Membership': f"SELECT * FROM Win32_ComputerSystem WHERE PartOfDomain = {value}",
            'User Role': f"SELECT * FROM Win32_OperatingSystem WHERE ProductType = {value}"
        },
        'Software and Applications': {
            'Installed Applications': f"SELECT * FROM Win32_Product WHERE Name = '{value}'",
            'Antivirus Status': "SELECT * FROM AntivirusProduct"
        },
        'System Uptime': {
            'Uptime': f"SELECT * FROM Win32_OperatingSystem WHERE LastBootUpTime < '{value}'"
        },
        'Power Settings': {
            'Battery Status': f"SELECT * FROM Win32_Battery WHERE BatteryStatus = {value}"
        },
        'Event Logs': {
            'Specific Event Logs': f"SELECT * FROM Win32_NTLogEvent WHERE Logfile = 'System' AND EventCode = {value}"
        }
    }

    return queries[category][option]

def main():
    print("Quickly Build your WMI Query")
    print("Follow the prompts and build away!.\n")

    # Available categories
    categories = [
        'Operating System Information', 'Hardware Information', 'Disk Space', 
        'Network Configuration', 'System Roles', 'Software and Applications', 
        'System Uptime', 'Power Settings', 'Event Logs'
    ]

    # Options within each category
    options = {
        'Operating System Information': ['Version', 'Service Pack Level'],
        'Hardware Information': ['Manufacturer', 'Model', 'Memory'],
        'Disk Space': ['Free Space on Logical Disks'],
        'Network Configuration': ['IP Address', 'DHCP Status'],
        'System Roles': ['Domain Membership', 'User Role'],
        'Software and Applications': ['Installed Applications', 'Antivirus Status'],
        'System Uptime': ['Uptime'],
        'Power Settings': ['Battery Status'],
        'Event Logs': ['Specific Event Logs']
    }

    # Display categories to the user
    for idx, category in enumerate(categories, 1):
        print(f"{idx}. {category}")

    category_idx = get_user_input(
        "\nSelect a category by number: ",
        r"^[1-9]$|^10$",
        "1"
    )
    category = categories[int(category_idx) - 1]

    print(f"\nYou selected: {category}")
    for idx, option in enumerate(options[category], 1):
        print(f"{idx}. {option}")

    option_idx = get_user_input(
        "\nSelect an option by number: ",
        r"^[1-9]$|^10$",
        "1"
    )
    option = options[category][int(option_idx) - 1]

    # Example values for guidance
    value_example = {
        'Version': "10.%",
        'Service Pack Level': "2",
        'Manufacturer': "Dell Inc.",
        'Model': "Latitude 5480",
        'Memory': "4294967296",
        'Free Space on Logical Disks': "C: 10737418240",
        'IP Address': "192.168.1.%",
        'DHCP Status': "TRUE",
        'Domain Membership': "TRUE",
        'User Role': "1",
        'Installed Applications': "Microsoft Office 2016",
        'Antivirus Status': "",
        'Uptime': "20230101000000.000000-000",
        'Battery Status': "2",
        'Specific Event Logs': "41"
    }

    # Antivirus Status doesn't require additional input
    if option == "Antivirus Status":
        value = ""
    else:
        value = get_user_input(
            f"\nEnter the value for {option} (e.g., {value_example[option]}): ",
            r".+",
            value_example[option]
        )

    # Create and display the WMI query
    query = create_wmi_query(category, option, value)
    print("\nYour WMI Query is:")
    print(query)

if __name__ == "__main__":
    main()
