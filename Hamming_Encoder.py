def hamming_encoder(data):
    m = len(data)
    
    
    r = 0
    while 2**r < m + r + 1:
        r += 1
    
    n = m + r  
    
    
    bits = ['_'] * (n + 1)
    
    
    for i in range(r):
        bits[2**i] = 'P'
    
    
    j = 0  
    for i in range(1, n + 1):
        if bits[i] != 'P':
            bits[i] = data[j]
            j += 1
    
    
    for i in range(r):
        pos = 2**i
        total = 0
        
        for k in range(1, n + 1):
            if k & pos == pos and bits[k] != 'P':
                total += int(bits[k])
        
        bits[pos] = '0' if total % 2 == 0 else '1'
    
    
    return ''.join(bits[1:])


#print(hamming_encoder("10110"))  # Output: 01100110
#print(hamming_encoder("1011"))   # Output: 0111011
