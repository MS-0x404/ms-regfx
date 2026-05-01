# ms-regfx

Parser and utilities for working with **Windows Registry (REGF)** files.

## 📌 Description

`ms-regfx` is a project designed to read, analyze, and manipulate Windows Registry files (REGF format). These files are used by Windows systems to store configuration data for the OS and installed applications.

## ✨ Features

* Parse registry hive files (e.g., `NTUSER.DAT`, `SYSTEM`)
* Navigate hierarchical keys and values
* Extract data types (strings, DWORD, binary, etc.)
* Access internal registry structures

## 📂 Project Structure

```
ms-regfx/
├── core/            # core of project
├── outputs/       # Many type of outputs
├── main.py        # Main file
└── README.md
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/MS-0x404/ms-regfx.git
cd ms-regfx
```

Install from AUR:

```bash
yay -S ms-regfx
regfx --help
```


## 🚀 Usage

Basic example:

```bash
# generic example 
regfx NTUSER.DAT run -r --csv
```

## 🛠️ Use Cases

* Forensic analysis of compromised systems
* Extracting artifacts (MRU, configuration data, etc.)
* Automating registry analysis


