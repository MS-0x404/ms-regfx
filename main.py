#!/usr/bin/env python3

import sys
from core.keys import KEYS
from core.parser import *
from core.parser_item import strip_prefix_from_item, flatten
from outputs.out_csv import *
from outputs.out_json import *


HEADER_REGF = 4096


def about_help():
    return """
Registry File Parser - ms-regfx (Help)

Usage:
  python main.py <input_file> <key> [options]
  regfx <input_file> <key> [options]

Arguments:
  <input_file>   Path to the input file (must be in REGF format).
  <key>          Key to search for in the registry. 

Options:
  --csv          Output results in CSV format.
  --json         Output results in JSON format.
  --recursive, -r  Search recursively in the registry.
  --help, -h     Show this help message.

Examples:
  python main.py NTUSER.DAT "Software\\Microsoft" --csv
  python main.py SAM "SAM\\Domains" --json
"""


def main(raw, header, key, recursive, reglista):
    path = key.split("\\")
    if recursive:
        result = cerca_chiave(raw, header["start_cell"], path, recursive)
    else:
        result = cerca_chiave(raw, header["start_cell"], path)
        
    if not result:
        print("Error: No value found! Check the key or try changing the file!")
        sys.exit(1)
    else:
        if "--csv" in sys.argv:
            csv_report(result)                
        elif "--json" in sys.argv:
            json_report(result)
                 


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        try:
            raw = open(sys.argv[1], "rb").read()
            formato = raw[:4]
            if formato != b'regf':
                print(f"Error: Unsupported format {formato}!")
                sys.exit(1)
        except FileNotFoundError:
            print("File not found!")
            sys.exit(1)
        header = leggi_header(raw)
        prefix = leggi_nk(raw, header["start_cell"])["named"]
        recursive = "--recursive" in sys.argv or "-r" in sys.argv
        
        reglista = lista_chiavi(raw, header["start_cell"])
        reglista = strip_prefix_from_item(reglista, prefix+"\\")
        reglista = flatten(reglista)
        

        key = sys.argv[2]
        nomi = [k for gruppo in KEYS.values() for k in gruppo.keys()]
        
        if key in nomi:
            for value in KEYS.values():
                if key in value:
                    path = value[key]
        elif key.lower() in reglista:
            path = key
        else:
            print("Error: Key not found!")
            sys.exit(1)
    elif "--help" in sys.argv or  "-h" in sys.argv:
        print(about_help())
        sys.exit(1)
    else:
        print("Error: No arguments provided. Use --help to see available options.")
        sys.exit(1)
    
    main(raw, header, path, recursive, reglista)
    

