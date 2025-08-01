import math
import numpy as np


### One-hot Encoders
def one_hot_encoder(message, message_set):
    if message not in message_set:
        raise ValueError("Message not found in message set.")
    index = message_set.index(message)
    num_bits = math.ceil(np.log2(len(message_set)))
    binary = bin(index)[2:].zfill(num_bits)
    return np.array([int(b) for b in binary])

### Intelligent 
def one_hot_encoder_I(index, message_set):
    num_bits = math.ceil(np.log2(len(message_set)))
    binary = bin(index)[2:].zfill(num_bits)
    return np.array([int(b) for b in binary])
  

def one_hot_decoder(binary_array, message_set):
    binary_str = ''.join(str(int(b)) for b in binary_array)
    index = int(binary_str, 2)
    if index >= len(message_set):
        raise ValueError("Decoded index is out of range.")
    return message_set[index]





### Parity bit
def parity_encoder(message, M_set):
  num = M_set.index(message)
  binary_num = bin(num)[2:]
  while len(binary_num) < 5:
    binary_num = "0" + binary_num
# adding the parity bit
  if binary_num.count("1") % 2 == 0: # if even 1s, end with 0
    binary_num = binary_num + "0"
  else:
    binary_num = binary_num + "1" # if odd 1s, end with 1
  print(binary_num)

#parity("Object collision detected", big_message_set)

def parity_decoder(received_bits_str):
  if received_bits_str[:5].count("1") % 2 == 0: # if even number of 1s, check for 0
    if received_bits_str[5] == '0':
      print("No error detected") # true
    else:
      print("Error detected") # false
  elif received_bits_str[:5].count("1") % 2 == 1: # if odd number of 1s, check for 1
    if received_bits_str[5] == '1':
      print("No error detected") # true
    else:
      print("Error detected") # false

