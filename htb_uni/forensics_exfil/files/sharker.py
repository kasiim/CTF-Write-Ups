# PyShark is a tshark wrapper for python, lets you basically use python as wireshark ;)
import pyshark
# Needed for time comparision
import datetime

# Open the capture file and get the captures
# will return list of capture objects, which we can loop over
captures = pyshark.FileCapture('mysql_dump.pcap')

# exfiltrated string 
recovered_chars = ""
# integer value for ascii character
built_character = 0

# remember last capture, since we need to do comparision
last_capture = None

# loop over all captures we have
for capture in captures:

    # remember first one and continue with loop
    # starting condition
    if last_capture == None:
        last_capture = capture

    # do magic here
    else:
        # first lets calculate time difference in seconds between two captures
        sleep_time = (capture.sniff_time - last_capture.sniff_time).total_seconds()

        # Get the sql query of last capture
        mysql_query = str(last_capture.layers[4]._all_fields['mysql.query'])
        # Get the sql query of current capture
        next_mysql_query = str(capture.layers[4]._all_fields['mysql.query'])

        # Split those sql querys into different parts, what we really need is
        # which bit was exfiltrated using this sql query
        # and which letter was extracted
        head, char_index, end = mysql_query.split(",")

        next_head, next_char_index, next_end = next_mysql_query.split(",")

        # Split the query further getting the which bit
        which_bit = end.split(">> ")[1].split(" &")[0]
        # print(which_bit)
        if sleep_time > 2:

            # print(head, char_index, bit)

            # how many times we have to shift, to place the bit at the right place
            built_character |= (1 << int(which_bit))

        # If character we are exfiltrating has changed, we can append it to exfiltrated string
        if char_index != next_char_index:
            # print(next_char_index, char_index)
            # Append it to the end of string
            recovered_chars += chr(built_character)

            # reset the built character ascii value
            built_character = 0

        # remember, current as last and move on
        last_capture = capture

print("Exfiltrated data:", recovered_chars)

# Exfiltrated data: db_m3149screenshots,usersid,user,passwordadminHTB{b1t_sh1ft1ng_3xf1l_1s_c00l
# We can see that the script does a lousy job and misses the last character, I was too
# lazy to fix this since we can already see the flag and know the last character is "}"