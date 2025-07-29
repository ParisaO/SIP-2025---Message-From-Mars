
import numpy as np
import matplotlib.pyplot as plt
from Source_Coding import one_hot_encoder, parity_encoder, hamming_encoder, decode_message
from Channel_Modulation import bpsk_modulate, bpsk_demodulate, qpsk_modulate, qpsk_demodulate
from Message_Set import get_message_set, message_to_index
from AWGN import add_awgn_noise

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


selected_encoder = "parity"      # Options: "one_hot", "parity", "hamming"
selected_modulator = "BPSK"      # Options: "BPSK", "QPSK"

encode = encoder_options[selected_encoder]
modulate, demodulate = modulator_options[selected_modulator]

# Load messages
messages = get_message_set()
ber_results = []

for snr_db in snr_dBs:
    total_errors = 0
    total_bits = 0

    for _ in range(num_trials):
        msg = np.random.choice(messages)
        idx = message_to_index(msg)
        bits = encode(idx)
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
