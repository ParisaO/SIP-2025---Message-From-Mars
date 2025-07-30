def message_to_index(message_set, message):
    binary_space = [format(i, '04b') for i in range(16)]
    
    # Unavailable binary strings
    invalid_codes = {"0001", "0010", "0100", "1011", "1101", "1110"}
    
    code_map = {}
    
    # Assign the emergency messages to '0000' and '1111'
    code_map[message_set[0]] = '0000'
    code_map[message_set[1]] = '1111'
    
    remaining_codes = [code for code in binary_space if code not in invalid_codes and code not in {'0000', '1111'}]

    msg_index = 2  # Start assigning from the third message
    for code in remaining_codes:
        if msg_index < len(message_set):
            code_map[message_set[msg_index]] = code
            msg_index += 1
        else:
            break  

    # Return the binary string for the given message
    return code_map.get(message, "Error: Message not in set")


binary_str = message_to_index(small_message, "Robot is overheating")
print(binary_str)  # Output should be '0111'
