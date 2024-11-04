import platform
import sys
import os

info_head = "[i] INFO: "
eror_head = "[i] EROR: "
misc_head = "[*] MISC: "
inpt_head = "[^] INPT: "

def get_inbetween(input_text, input_starting_point, input_ending_point):
    start_index = input_text.find(input_starting_point)
    end_index = input_text.find(input_ending_point, start_index + len(input_text))
    if start_index != -1 and end_index != 1:
        return input_text[start_index + len(input_starting_point):end_index]
    else:
        print(f"{eror_head}index for get_inbetween returned -1, ending script.")
        exit(1)

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
            raw_shell_code.append(byte.hex())
            byte = file.read(1)
        file.close()
    print(f"{misc_head}Creating a hex form of \'shellcode.bin\'...")
    with open("hex_shellcode.txt", 'w') as file:
        for byte in raw_shell_code:
            file.write(f"{byte}\n")
        file.close()
    print(f"{misc_head}Wrote hex for of \'shellcode.bin\' to \'hex_shellcode.txt\'.")
if __name__ == '__main__':
    try:
        import pefile
    except:
        with open("requirements.txt", "w") as file:
            file.write("pefile==2023.2.7\n")
            file.close()
        print(f"{info_head}Installing needed package \'pefile\'...")
        if 'Windows' in platform.platform():
            os.system('python -m pip install -r requirements.txt')
        else:
            os.system('pip3 install -r requirements.txt')
        print(f"{info_head}Installed package \'pefile\'.")
    import pefile
    if len(sys.argv) != 2:
        print(f"{info_head}usage: python(3) ErroxShell.py <exe_file_path>")
        exit(1)
    exe_path = sys.argv[1]
    extract_shell_code(exe_path)
