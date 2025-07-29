def hamming_decoder(encoded):
    n = len(encoded)

 
    r = 0
    while 2**r < n + 1:
        r += 1

    
    bits = ['_'] + [str(b) for b in encoded]  


    error_pos = 0
    for i in range(r):
        parity_pos = 2**i
        total = 0
        for k in range(1, n + 1):
            if k & parity_pos:
                total += int(bits[k])
        if total % 2 != 0:
            error_pos += parity_pos

    

    if error_pos != 0 and error_pos <= n:
        bits[error_pos] = '1' if bits[error_pos] == '0' else '0'


    data_bits = []
    for i in range(1, n + 1):
        if (i & (i - 1)) != 0:
            data_bits.append(str(bits[i]))  

    return ''.join(data_bits), error_pos
