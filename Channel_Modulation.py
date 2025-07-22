import numpy as np



#BPSK Modulation
def bpsk_modulate(bits):
    bit_array = np.array(list(bits), dtype=int) # Convert characters to integers
    bpsk_symbols = 2 * bit_array - 1
    return bpsk_symbols

# print(bpsk_modulate('10101'))


#BPSK Demodulation
def bpsk_demodulate(received):
  recieved = np.array(received)
  bpsk_array = []
  for i in received:
    if (i < 0):
      bpsk_array.append(0)
    if (i > 0):
      bpsk_array.append(1)
  return np.array(bpsk_array)
  
# print(bpsk_demodulate([1, -1, 1, -1, 1]))


# QPSK Modulation
def qpsk_modulate(bits):
   bits = bits.reshape(-1, 2)
   mapping = {
       (0, 0): (-1, -1),
       (0, 1): (-1, 1),
       (1, 0): (1, -1),
       (1, 1): (1, 1)
   }
   symbols = np.array([mapping[tuple(b)] for b in bits]) * (A / np.sqrt(2))
   return symbols


#QPSK Demodulation
def qpsk_demodulate(received):
   A = 1
   received /= (A / np.sqrt(2))
   bits = []
   for r in received:
       bits.extend([
           (r.real > 0).astype(int),
           (r.imag > 0).astype(int)
       ])
   return np.array(bits)
