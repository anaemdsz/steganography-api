
def nth_bit_present(byte, n):
    # Bitwise check to see what the nth bit is
    # If we get anything other than 0, it is TRUE else FALSE
    return (byte & (1 << n)) != 0

def set_lsb(bmp_byte, bit):
    new_byte = 0
    if bit:
        if (nth_bit_present(bmp_byte, 0)):
            new_byte = bmp_byte  # No modification needed, it already ends in one
        else:
            new_byte = bmp_byte + 1
    else:
        if (nth_bit_present(bmp_byte, 0)):
            new_byte = bmp_byte - 1
        else:
            new_byte = bmp_byte  # No modification needed, it already ends in zero
    return new_byte

def bits_to_byte(bits):
	assert len(bits) == 8
	new_byte = 0
	for i in range(8):
		if bits[i]==True:
			#This bit==1 and the "position" we are at in the byte is 7-i
			#Bitwise OR will insert a 1 a this position
			new_byte |= 1 << 7 - i
		else:
			#This bit==0 and the "position" we are at in the byte is 7-i
			#Bitwise OR will insert a 0 a this position
			new_byte |= 0 << 7 - i
            
	return new_byte