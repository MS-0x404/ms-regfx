KEYS = {
    "ntuser": {
        "run": "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",
        "userassist": "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist",
        "recentdocs": "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RecentDocs",
        "shellbags": "SOFTWARE\\Microsoft\\Windows\\Shell\\BagMRU",
        "typedurl": "Software\\Microsoft\\Internet Explorer\\TypedURLs",
        "winlogon": "Software\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon",
        "comdlg32": "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\OpenSaveMRU",
    },
    "software": {
        "muicache": "LOCAL SETTINGS\\Software\\Microsoft\\Windows\\Shell\\MuiCache",
        "installed": "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
        "network": "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\NetworkList\\Profiles",
        "version": "Microsoft\\Windows NT\\CurrentVersion",
        "windows": "ControlSet001\\Control\\Windows",
    },
    "system": {
        "usbstor": "ControlSet001\\Enum\\USBSTOR",
        "mounted": "MountedDevices",
        "hostname": "ControlSet001\\Control\\ComputerName\\ComputerName",
        "timezone": "ControlSet001\\Control\\TimeZoneInformation",
        "syskey": "ControlSet001\\Control\\Lsa",
    },
    "sam": {
        "accounts": "SAM\\Domains\\Account\\Users\\Names",
    }
}
