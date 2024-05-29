def convert_mp3_to_header(input_file, output_file):
    with open(input_file, 'rb') as f:
        byte_array = f.read()
    
    with open(output_file, 'w') as f:
        f.write("const unsigned char audioData[] = {\n")
        for i, byte in enumerate(byte_array):
            if i % 12 == 0:
                f.write("\n")
            f.write(f"0x{byte:02x}, ")
        f.write("\n};\n")
        f.write(f"const unsigned int audioDataLen = {len(byte_array)};\n")

# Use raw strings to avoid escape sequence issues
input_file = r'C:\Meet\ESP32\Karnali_Speaker System\Speaker_Sys_Test_1.8\Speaker_Sys_Test_1.8\data\Husn.mp3'  # Change this to your MP3 file
output_file = r'C:\Meet\ESP32\Karnali_Speaker System\Speaker_Sys_Test_1.8\Speaker_Sys_Test_1.8\data\audio.h'
convert_mp3_to_header(input_file, output_file)
