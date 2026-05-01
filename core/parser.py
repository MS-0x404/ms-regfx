import sys
import struct
import codecs
import datetime

def leggi_header(raw):
    header = raw[:4096]
    root_cell = struct.unpack("<I", header[36:40])
    start_cell = len(header) + root_cell[0]
    lenght_cell = struct.unpack("<i", raw[start_cell : start_cell+4])
    if lenght_cell[0] > 0:
        print("File corrotto!")
        sys.exit(1)
    return {"header":header, 
            "root_cell":root_cell, 
            "start_cell":start_cell, 
            "lenght_cell":lenght_cell
            }

def leggi_nk(raw, offset):
    named_firma = raw[offset+4:offset+4+2]
    lenght_name = struct.unpack("<H", raw[offset+76 : offset+78])
    subkeys = struct.unpack("<I", raw[offset+24 : offset+24+4])
    flags = struct.unpack("<H", raw[offset+6 : offset+6+2])
    if flags[0] & 0x0020:
        try:
            named = raw[offset+80 : offset+80+lenght_name[0]].decode("ascii")
        except UnicodeDecodeError:
            named = raw[offset+80 : offset+80+lenght_name[0]].decode("latin-1")
    else:
        named = raw[offset+80 : offset+80+lenght_name[0]].decode("utf-16-le").rstrip("\x00")
    offset_keys = struct.unpack("<I", raw[offset+32 : offset+32+4])
    num_valori = struct.unpack("<I", raw[offset+40 : offset+40+4])
    offset_valori = struct.unpack("<I", raw[offset+44 : offset+44+4])
    return {"named_firma":named_firma, 
            "lenght_name":lenght_name, 
            "named": named,
            "flags": flags,
            "subkeys":subkeys, 
            "offset_keys": offset_keys,
            "num_valori": num_valori,
            "offset_valori": offset_valori
            }

def leggi_dati(raw, offset_data, lenght_data, type_data):
    if type_data == 1: # REG_SZ
        if lenght_data & 0x80000000:
            # inline
            lunghezza_vera = lenght_data & 0x7FFFFFFF
            data = struct.pack("<I", offset_data)[:lunghezza_vera].decode("utf-16-le")
        else:
            # offset
            data_offset = 4096 + offset_data + 4
            try:
               data = raw[data_offset : data_offset+lenght_data].decode("utf-16-le").rstrip("\x00")
            except UnicodeDecodeError:
                data = raw[data_offset : data_offset+lenght_data].hex()
    elif type_data == 2: # REG_EXPAND_SZ
        if lenght_data & 0x80000000:
            lunghezza_vera = lenght_data & 0x7FFFFFFF
            data = struct.pack("<I", offset_data)[:lunghezza_vera].decode("utf-16-le")
        else:
            data_offset = 4096 + offset_data + 4
            try:
                data = raw[data_offset : data_offset+lenght_data].decode("utf-16-le").rstrip("\x00")
            except UnicodeDecodeError:
                data = raw[data_offset : data_offset+lenght_data].hex()
    elif type_data == 3: # REG_BINARY
        if lenght_data & 0x80000000:
            lunghezza_vera = lenght_data & 0x7FFFFFFF
            data = struct.pack("<I", offset_data)[:lunghezza_vera].hex()
        else:
            pos = 4096 + offset_data + 4
            data = raw[pos : pos+lenght_data].hex()
    elif type_data == 4: # REG_DWORD
        if lenght_data & 0x80000000:
            data = offset_data
        else:
            pos = 4096 + offset_data
            data = struct.unpack("<I", raw[pos : pos+4])[0]
    elif type_data == 7:  # REG_MULTI_SZ
        if lenght_data & 0x80000000:
            lunghezza_vera = lenght_data & 0x7FFFFFFF
            raw_bytes = struct.pack("<I", offset_data)[:lunghezza_vera]
        else:
            data_offset = 4096 + offset_data + 4
            raw_bytes = raw[data_offset : data_offset+lenght_data]
            try:
                stringhe = raw_bytes.decode("utf-16-le").split("\x00")
                data = " | ".join(s for s in stringhe if s)
            except UnicodeDecodeError:
                data = raw_bytes.hex()
    else:
        if lenght_data & 0x80000000: # Default
            lunghezza_vera = lenght_data & 0x7FFFFFFF
            data = struct.pack("<I", offset_data)[:lunghezza_vera].hex()
        else:
            pos = 4096 + offset_data
            data = raw[pos : pos+lenght_data].hex()
    return data
    

def leggi_vk(raw, offset):
    firma = raw[offset+4 : offset+6]
    lenght_name = struct.unpack("<H", raw[offset+6 : offset+6+2])
    flags = struct.unpack("<H", raw[offset+20 : offset+20+2])
    if flags[0] & 0x0001:
        try:
            name_vk = raw[offset+24 : offset+24+lenght_name[0]].decode("ascii")
        except UnicodeDecodeError:
            name_vk = raw[offset+24 : offset+24+lenght_name[0]].decode("latin-1")
    else:
        name_vk = raw[offset+24 : offset+24+lenght_name[0]].decode("utf-16-le").rstrip("\x00")
    lenght_data = struct.unpack("<I", raw[offset+8 : offset+8+4])
    offset_data = struct.unpack("<I", raw[offset+12 : offset+12+4])
    type_data = struct.unpack("<I", raw[offset+16 : offset+16+4])
    
    
    return {"firma":firma, 
            "lenght_name":lenght_name, 
            "lenght_data":lenght_data, 
            "offset_data":offset_data, 
            "type_data":type_data, 
            "name_vk":name_vk
            }

def decode_recentdocs(hex_data):
    raw = bytes.fromhex(hex_data)
    try:
        end = raw.find(b"\x00\x00")
        if end == -1:
            return None

        name = raw[:end+2].decode("utf-16le", errors="ignore")
        return name
    except:
        return None
def parse_mru(hex_data):
    raw = bytes.fromhex(hex_data)
    order = []

    for i in range(0, len(raw), 4):
        val = int.from_bytes(raw[i:i+4], "little")
        if val == 0xFFFFFFFF:
            break
        order.append(val)

    return order

def decode_shell_item(hex_data):
    raw = bytes.fromhex(hex_data)
    size = struct.unpack("<H", raw[0:2])[0]
    tipo = raw[2]
    GUID_MAP = {
    "80531c87a0426910a2ea08002b30309d": "My Computer",
    "e04fd020ea3a6910a2d808002b30309d": "Desktop",
    "ba8f0d4525add01198a80800361b1103": "Network Neighborhood",
    "2020ec21ea3a6910a2dd08002b30309d": "My Network Places",
    }  
    if tipo == 0x1F:   
        guid = raw[4:20].hex()
        name = GUID_MAP.get(guid, f"[Special Folder: {guid}]")
    elif tipo == 0x2E:
        guid = raw[4:20].hex()
        name = GUID_MAP.get(guid, f"[Network: {guid}]")
    elif tipo == 0x31 or tipo == 0x32:
        fine = raw.index(b'\x00', 14)
        dos_name = raw[14:fine].decode("ascii", errors="replace")
        sig = b'\x04\x00\xef\xbe'
        idx = raw.find(sig)

        fat_date = struct.unpack("<H", raw[idx+8:idx+10])[0]
        fat_time = struct.unpack("<H", raw[idx+10:idx+12])[0]
        year = ((fat_date >> 9) & 0x7F) + 1980
        month = (fat_date >> 5) & 0x0F
        day = fat_date & 0x1F
        hour = (fat_time >> 11) & 0x1F
        minute = (fat_time >> 5) & 0x3F
        second = (fat_time & 0x1F) * 2

        timestamp = f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"


        inizio_lungo = idx + 16
        i = inizio_lungo
        while i < len(raw) - 1:
            if raw[i] == 0 and raw[i+1] == 0:
                fine_lungo = i
                break
            i += 2
        name = raw[inizio_lungo:fine_lungo].decode("utf-16-le").rstrip("\x00")
        name = f"{name} [{timestamp}]" 
    return name


def visita_nk(raw, offset, profondita=0, percorso=""):
    nk = leggi_nk(raw, offset)
    print("  " * profondita + nk["named"])
    if nk["num_valori"][0] > 0 and nk["offset_valori"][0] != 0xFFFFFFFF:
        offset_lista_val = nk["offset_valori"][0] + 4096
        for i in range(nk["num_valori"][0]):
            vk_rel = struct.unpack("<I", raw[offset_lista_val+4+(i*4):offset_lista_val+8+(i*4)])[0]
            vk_ass = vk_rel + 4096
            vk = leggi_vk(raw, vk_ass)
            nome = vk["name_vk"] if vk["name_vk"] else "(Default)"
            dato = leggi_dati(raw, vk["offset_data"][0], vk["lenght_data"][0], vk["type_data"][0])
            if "RecentDocs" in percorso:
                if nome == "MRUListEx":
                    dato = parse_mru(dato)
                elif nome.isdigit():
                    decoded = decode_recentdocs(dato)
                    if decoded:
                        dato = decoded
            if "BagMRU" in percorso or "BagMRU" in nk["named"]:
                if nome == "MRUListEx":
                    dato = parse_mru(dato)
                elif nome.isdigit():
                    dato = decode_shell_item(dato)
            if nk["named"] == "Count" and "UserAssist" in percorso:
                nome = codecs.decode(nome, "rot_13")
                b = bytes.fromhex(dato)
                count = struct.unpack("<I", b[4:8])[0]
                ft = int.from_bytes(b[8:16], "little")
                dt = datetime.datetime(1601,1,1) + datetime.timedelta(microseconds=ft//10)
                dato = f"eseguito {count} volte, ultimo avvio {dt}"
            print("  " * (profondita+1) + f"{nome} = {dato}")

    if nk["subkeys"][0] > 0 and nk["offset_keys"][0] != 0xFFFFFFFF:
        offset_lista = nk["offset_keys"][0] + 4096
        subkeys = lista_subkeys(raw, offset_lista)
        for off in subkeys:
            visita_nk(raw, off + 4096, profondita + 1, percorso + "\\" + nk["named"])


def lista_subkeys(raw, offset_lista):
    firma = raw[offset_lista+4 : offset_lista+6]
    list_start = struct.unpack("<H", raw[offset_lista+6 : offset_lista+8])[0]
    offset_nk = []
    
    if firma == b'lf' or firma == b'lh':
        for i in range(list_start):
            result = struct.unpack("<I", raw[offset_lista+8+(i*8) : offset_lista+12+(i*8)])
            offset_nk.append(result[0])
    elif firma == b'li':
        for i in range(list_start):
            result = struct.unpack("<I", raw[offset_lista+8+(i*4) : offset_lista+12+(i*4)])
            offset_nk.append(result[0])
    elif firma == b'ri':
        for i in range(list_start):
            sublista_rel = struct.unpack("<I", raw[offset_lista+8+(i*4):offset_lista+12+(i*4)])[0]
            sublista_ass = sublista_rel + 4096
            offset_nk += lista_subkeys(raw, sublista_ass)
            
            

    return offset_nk
    

def stampa_valori(raw, offset, percorso=""):
    nk = leggi_nk(raw, offset)
    print(f"Chiave: {nk['named']}")
    risultato = {"chiave": nk["named"], "valori": []}
    if nk["num_valori"][0] > 0 and nk["offset_valori"][0] != 0xFFFFFFFF:
        offset_lista_val = nk["offset_valori"][0] + 4096
        for i in range(nk["num_valori"][0]):
            vk_rel = struct.unpack("<I", raw[offset_lista_val+4+(i*4) : offset_lista_val+8+(i*4)])[0]
            vk_ass = vk_rel + 4096
            vk = leggi_vk(raw, vk_ass)
            dato = leggi_dati(raw, vk["offset_data"][0], vk["lenght_data"][0], vk["type_data"][0])
            nome = vk["name_vk"] if vk["name_vk"] else "(Default)"

            if "RecentDocs" in percorso or "RecentDocs" in nk["named"]:
                if nome == "MRUListEx":
                    dato = parse_mru(dato)
                elif nome.isdigit():
                    decoded = decode_recentdocs(dato)
                    if decoded:
                        dato = decoded
            if "BagMRU" in percorso or "BagMRU" in nk["named"]:
                if nome == "MRUListEx":
                    dato = parse_mru(dato)
                elif nome.isdigit():
                    dato = decode_shell_item(dato)
            risultato["valori"].append({"nome": nome, "dato": dato})
            print(f"  {nome} = {dato}")
    return risultato

def lista_chiavi(raw, offset, pathfull=""):
    nk = leggi_nk(raw, offset)
    if pathfull:
        percorso = pathfull + "\\" + nk["named"]
    else:
        percorso = nk["named"]

    result = [percorso]
    
    if nk["subkeys"][0] > 0 and nk["offset_keys"][0] != 0xFFFFFFFF:
        offset_lista = nk["offset_keys"][0] + 4096
        subkeys = lista_subkeys(raw, offset_lista)
        for off in subkeys:
            figli = lista_chiavi(raw, off + 4096, percorso)
            result.extend(figli)
    return [result]

def cerca_chiave(raw, offset, path, recursive=False, path_origin=""):
    nk = leggi_nk(raw, offset)
    if len(path) == 0:
        if recursive:
            visita_nk(raw, offset, percorso=path_origin)
            result = True
        else:
            # leggi i valori
            result = stampa_valori(raw, offset, path_origin)
        return result
    if nk["subkeys"][0] > 0 and nk["offset_keys"][0] != 0xFFFFFFFF:
        offset_lista = nk["offset_keys"][0] + 4096
        subkeys = lista_subkeys(raw, offset_lista)
        for off in subkeys:
            nk_figlia = leggi_nk(raw, off + 4096)
            if nk_figlia["named"].lower() == path[0].lower():
                return cerca_chiave(raw, off + 4096, path[1:], recursive, path_origin + "\\" + path[0])
    


    



