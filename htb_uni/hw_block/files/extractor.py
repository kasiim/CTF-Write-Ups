# Information from serial communication
# will use later in the code
flash_locations = ["14", "17", "27", "11", "04", "15", "19", "40", "21", "51", "18", "06", "49", "02", "31", "50", "28", "41", "32", "35", "24", "39", "42", "36", "45", "03", "43", "20", "00", "01", "09", "44", "38", "07", "22", "08", "13", "23", "37", "10", "47", "05", "33", "26", "46", "25"]

# We know that we had 16 pages of memory
# 16 * 4096 = 65536 bytes which is our file size.

# Open the file as binary
with open("dump.bin", "rb") as binary_file:
    bytes_from_file = binary_file.read()

# So now is a good idea to explain what we found from sequence.logicdata
# After init it tells how flash is read:
# We have following information "'Comm..xy' 'sector:xCOMMA' 'page:yCOMMA' 'page_offset:xy"
# We can see that it uses x as sector and y as page, also it tells that page_offset is xy
# So x value is for sector, since we have 4096 bytes in sector
# we get address by multiplying x by that value
# y goes for pages so 256 bytes per page, we multiply y by that.
# Finally we have page offset which tells us which byte is read.

# Now we loop over all locations we got and build address formula
# Print out bytes and hopefully enjoy the flag ;)
for location in flash_locations:
    x, y = int(location[0]), int(location[1])

    # This is formula for finding the right bytes to be read
    address = 4096 * x + 256 * y + int(location)
    
    print(chr(bytes_from_file[address]), end='')
print()


# Flag is HTB{M3m0ry_5cR4mbl1N6_c4n7_54v3_y0u_th1S_t1M3}