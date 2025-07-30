
import numpy as np
import matplotlib.pyplot as plt
from Source_Coding import one_hot_encoder, one_hot_decoder, parity_encoder, parity_decoder    # Add Hamming
from Hamming_Decoder import hamming_decoder
from Hamming_Encoder import hamming_encoder
from Channel_Modulation import bpsk_modulate, bpsk_demodulate, qpsk_modulate, qpsk_demodulate
from message_to_index import message_to_index    
from AWGN import add_awgn_noise


small_message_set = ["Battery level is critical",
"Object collision detected",
"Robot is overheating",
"Robot is 10 feet from object",
"System malfunction",
"New foreign substance detected",
"Robot has gathered soil sample",
"Abnormal weather detected",
"Collected samples are ready for analyzation",
"Robot has found water source"]

big_message_set = ["Battery level is critical",
"Object collision detected",
"Robot is overheating",
"Robot is 10 feet from object",
"System malfunction",
"New foreign substance detected",
"Robot has gathered soil sample",
"Abnormal weather detected",
"Collected samples are ready for analyzation",
"Robot has found water source",
"Robot’s deviates significantly from path",
"Robot is stuck in a pitfall",
"Robot’s camera is damaged",
"Robot has encountered unknown object",
"Robot has analyzed atmospheric composition",
"Progress update: x% completed",
"Robot has removed space junk",
"Robot has taken an image of its surroundings",
"Strong winds detected",
"Robot’s current location is (x,y,z)"]




# Configuration
snr_dBs = [0, 2, 4, 6, 8, 10]
num_trials = 1000


## encoder and channel modulator options: 
encoder_options = {
    "one_hot": one_hot_encoder,
    "parity": parity_encoder,
    "hamming": hamming_encoder
}

modulator_options = {
    "BPSK": (bpsk_modulate, bpsk_demodulate),
    "QPSK": (qpsk_modulate, qpsk_demodulate)
}


selected_encoder = "one_hot"      # Options: "one_hot", "parity", "hamming"
selected_modulator = "BPSK"      # Options: "BPSK", "QPSK"

encode = encoder_options[selected_encoder]
modulate, demodulate = modulator_options[selected_modulator]

# Load messages
messages = small_message_set    ## Choose one message set here
ber_results = []

for snr_db in snr_dBs:
    total_errors = 0
    total_bits = 0

    for _ in range(num_trials):
        msg = np.random.choice(messages)
        messages = messages[0]
        idx = message_to_index(msg)
        bits = encode(idx, messages)    # bits = 0101
        signal = modulate(bits)
        noisy_signal = add_awgn_noise(signal, snr_db)
        received_bits = demodulate(noisy_signal)
        decoded_idx = decode_message(received_bits, method=selected_encoder)    

        bit_errors = np.sum(bits != received_bits[:len(bits)])
        total_errors += bit_errors   
        total_bits += len(bits)   

    ber = total_errors / total_bits     
    ber_results.append(ber)
    print(f"SNR={snr_db} dB, BER={ber:.4f}")


## Plotting
plt.plot(snr_dBs, ber_results, marker='o', label=f"{selected_encoder} + {selected_modulator}")
plt.xlabel("SNR (dB)")
plt.ylabel("Bit Error Rate (BER)")
plt.title("BER vs SNR")
plt.grid(True)
plt.legend()
plt.show()
