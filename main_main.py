import numpy as np
import matplotlib.pyplot as plt
from Source_Coding import one_hot_encoder, one_hot_decoder, parity_encoder, parity_decoder
from Hamming_Decoder import hamming_decoder
from Hamming_Encoder import hamming_encoder
from Channel_Modulation import bpsk_modulate, bpsk_demodulate, qpsk_modulate, qpsk_demodulate
from message_to_index import indexr
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
# snr_dBs = [0, 2, 4, 6, 8, 10, 15, 17.5, 20]
snr_dBs =[2,4,6,8,10]
num_trials = 1000

## encoder and channel modulator options:
encoder_options = {
    "one_hot": (one_hot_encoder, one_hot_decoder),
    "parity": (parity_encoder, parity_decoder),
    "hamming": (hamming_encoder, hamming_decoder)
}
modulator_options = {
    "BPSK": (bpsk_modulate, bpsk_demodulate),
    "QPSK": (qpsk_modulate, qpsk_demodulate)
}

selected_encoder = "one_hot"  # Options: "one_hot", "parity", "hamming"
selected_modulator = "BPSK"  # Options: "BPSK", "QPSK"
bits_per_symbol = 1
smart = False
ber_results = []

encoder, decoder = encoder_options[selected_encoder]
modulate, demodulate = modulator_options[selected_modulator]
messages = small_message_set

# Non - Smart
for snr_db in snr_dBs:
    total_errors = 0
    total_bits = 0
    idx = None

    for n in range(num_trials):
        msg = np.random.choice(messages)
        # print("The Generated message: ", msg, "At iteration ", n)
        if smart:
            idx = int(indexr(messages, msg, "encode"), 2)

        bits, idx = encoder(msg, messages, idx, smart)
        signal = modulate(bits)
        noisy_signal = add_awgn_noise(signal, snr_db, bits_per_symbol)
        received_bits = demodulate(noisy_signal)
        decoded_msg = decoder(received_bits, messages, smart)  # We don't really care about this...

        bit_errors = np.sum(bits != received_bits[:len(bits)])
        total_errors += bit_errors
        total_bits += len(bits)

    ber = total_errors / total_bits
    ber_results.append(ber)
    print(f"SNR={snr_db} dB, BER={ber:.4f}")

#
selected_encoder_2 = "one_hot"  # Options: "one_hot", "parity", "hamming"
selected_modulator_2 = "QPSK"
bits_per_symbol = 2
smart_2 = False
ser_results_qpsk = []
ber_results_qpsk = []

encoder, decoder = encoder_options[selected_encoder_2]
modulate, demodulate = modulator_options[selected_modulator_2]


for snr_db in snr_dBs:
    symbol_errors = 0
    total_bits = 0
    total_errors = 0
    idx = None

    for n in range(num_trials):
        msg = np.random.choice(messages)
        if smart:
            idx = int(indexr(messages, msg, "encode"), 2)

        bits, idx = encoder(msg, messages, idx, smart_2)
        signal = modulate(bits)
        noisy_signal = add_awgn_noise(signal, snr_db, bits_per_symbol)
        received_bits = demodulate(noisy_signal)
        decoded_msg = decoder(received_bits, messages, smart_2)

        bit_errors = np.sum(bits != received_bits[:len(bits)])
        total_bits += len(bits)
        total_errors += bit_errors

        if decoded_msg != msg:
            symbol_errors += 1

    ber = total_errors / total_bits
    ber_results_qpsk.append(ber)

    ser = symbol_errors / num_trials
    ser_results_qpsk.append(ser)
    print(f"SNR={snr_db} dB, SER={ser:.4f}")

# Plotting both smart and non-smart results
plt.plot(snr_dBs, ber_results, marker='o', label=f"{selected_encoder} with {selected_modulator} - smart: {smart}")
plt.plot(snr_dBs, ber_results_qpsk, marker='s',
         label=f"{selected_encoder_2} with {selected_modulator_2} - smart: {smart_2}")
plt.plot(snr_dBs, ser_results_qpsk, marker='^',
         label=f"{selected_encoder_2} with {selected_modulator_2} - smart: {smart_2} SER")

plt.xlabel("SNR (dB)")
plt.ylabel("Bit Error Rate (BER)")
plt.title("BER vs SNR")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
