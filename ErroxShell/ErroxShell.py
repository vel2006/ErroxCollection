import threading
import platform
import random
import time
import sys
import os

inpt_head = "\033[33m[^] INPT: \033[0m"
info_head = "\033[32m[i] INFO: \033[0m"
eror_head = "\033[31m[!] EROR: \033[0m"
misc_head = "\033[30m[*] MISC: \033[0m"

def gen_xor_key():
    print(f"{info_head}Creating key...")
    print(f"{misc_head}Getting values...")
    nano_system_time = time.time_ns()
    nano_process_time = time.process_time_ns()
    print(f"{misc_head}Doing a random length sleep for more randomness...")
    time.sleep(random.randint(0, random.randint(1, 10)))
    nano_thread_time = time.thread_time_ns()
    thread_id = threading.get_ident()
    cpu_state = int(psutil.cpu_percent(interval=1))
    allowed_selections = [nano_system_time, nano_process_time, nano_thread_time, thread_id, cpu_state]
    picked_selections = []
    print(f"{misc_head}Gotten values.")
    print(f"{misc_head}Orginizing values...")
    for i in range(len(allowed_selections)):
        choice = random.choice(allowed_selections)
        picked_selections.append(choice)
        allowed_selections.remove(choice)
    print(f"{misc_head}Done orginizing values.")
    print(f"{misc_head}Getting long key...")
    temp = ((picked_selections[0] ^ picked_selections[1]) ^ picked_selections[2]) ^ picked_selections[3] * picked_selections[4]
    temp = temp.to_bytes((temp.bit_length() + 7) // 8, 'big')
    print(f"{misc_head}Dont getting long key.")
    print(f"{misc_head}Converting long key into bytes...")
    key_array = []
    for byte in temp:
        temp_value = "0x{:02X}(".format(byte)
        key_array.append(temp_value[temp_value.find("x") + len("x"):temp_value.find("(", temp_value.find("x") + len("x") + len(temp_value))])
    print(f"{misc_head}Converted long key into bytes.")
    print(f"{misc_head}Picking random byte from bytes to be key...")
    key = random.choice(key_array)
    print(f"{info_head}Created key.")
    return key

def xor_encryption(input_data, key):
    output_array = []
    print(f"{info_head}Starting XOR encryption on data...")
    for byte in input_data:
        output_array.append(format(int(byte, 16) ^ int(key, 16), "02X"))
    print(f"{info_head}Done doing XOR encryption on data.")
    return output_array

def extract_shell_code(target_file):
    print(f"{info_head}Starting extraction of shell code...")
    print(f"{misc_head}Getting section offsets and info...")
    data_section_data_size = None
    data_section_pointer = None
    text_section_pointer = None
    text_section_data_size = None
    pef = pefile.PE(target_file)
    for section in pef.sections:
        pass
        section_data = str(section)
        for line in section_data.splitlines():
            words = line.split()
            for word in words:
                match word:
                    case '.text':
                        data_section_data_size = section.SizeOfRawData
                        text_section_pointer = section.PointerToRawData
                    case '.data':
                        text_section_data_size = section.SizeOfRawData
                        data_section_pointer = section.PointerToRawData
                    case _:
                        continue
    print(f"{misc_head}Gathered section info and offsets.")
    print(f"{misc_head}Creating shell code...")
    data_section_data = pef.get_data(data_section_pointer, data_section_data_size)
    text_section_data = pef.get_data(text_section_pointer, text_section_data_size)
    shell_code = text_section_data + data_section_data
    print(f"{misc_head}Created shell code.")
    print(f"{misc_head}Saving shell code to \'shellcode.bin\'...")
    with open("shellcode.bin", 'wb') as file:
        file.write(shell_code)
        file.close()
    print(f"{info_head}Saved shell code to \'shellcode.bin\'.")
    print(f"{misc_head}Reading \'shellcode.bin\'...")
    raw_shell_code = []
    with open("shellcode.bin", 'rb') as file:
        byte = file.read(1)
        while byte:
            raw_shell_code.append(byte.hex().upper())
            byte = file.read(1)
        file.close()
    print(f"{misc_head}Creating a hex form of \'shellcode.bin\'...")
    with open("hex_shellcode.txt", 'w') as file:
        for byte in raw_shell_code:
            file.write(f"{byte}\n")
        file.close()
    print(f"{misc_head}Wrote hex for of \'shellcode.bin\' to \'hex_shellcode.txt\'.")
    key = gen_xor_key()
    encrypted_hex_shell_code = xor_encryption(raw_shell_code, key)
    print(f"{misc_head}Writing XOR encrypted hex to \'encrypted_hex.txt\'...")
    with open("encrypted_hex.txt", 'w') as file:
        for byte in encrypted_hex_shell_code:
            file.write(f"{byte}\n")
        file.close()
    print(f"{misc_head}Wrote XOR encrypted hex to \'encrypted_hex.txt\'.")
    print(f"{misc_head}Checking for reverseability on XOR encrypted hex...")
    reversed_encrypted_hex_shell_code = xor_encryption(encrypted_hex_shell_code, key)
    if reversed_encrypted_hex_shell_code == encrypted_hex_shell_code:
        print(f"{misc_head}Encrypted XOR hex is reversable.")
    else:
        print(f"{eror_head}Encrypted XOR hex is not reversable.")

if __name__ == '__main__':
    print(" _____                     ____  _          _ _ ")
    print("| ____|_ __ _ __ _____  __/ ___|| |__   ___| | |")
    print("|  _| | '__| '__/ _ \\ \\/ /\\___ \\| '_ \\ / _ \\ | |")
    print("| |___| |  | | | (_) >  <  ___) | | | |  __/ | |")
    print("|_____|_|  |_|  \\___/_/\\_\\|____/|_| |_|\\___|_|_|")
    print("                         By: That1EthicalHacker")
    print("")
    try:
        import pefile
        import psutil
    except:
        with open("requirements.txt", "w") as file:
            file.write("pefile==2023.2.7\npsutil==6.0.0\n")
            file.close()
        print(f"{info_head}Installing needed packages \'pefile\' and \'psutil\'...")
        if 'Windows' in platform.platform():
            os.system('python -m pip install -r requirements.txt')
        else:
            os.system('pip3 install -r requirements.txt')
        print(f"{info_head}Installed package \'pefile\'.")
    import pefile
    import psutil
    if len(sys.argv) != 2:
        print(f"{error_head}Usage: python(3) ErroxShell.py <exe_file_path>")
        exit(1)
    exe_path = sys.argv[1]
    extract_shell_code(exe_path)
