import numpy as np
def add_awgn_noise(symbols, snr_db, mean):
  symbols = np.array(symbols)
  
  linear_snr = 10 ** (snr_db/10)
  signal_power = np.mean(np.abs(symbols)**2)
  noise_power = signal_power/linear_snr
  noise_std = np.sqrt(noise_power)

  noise = np.random.normal(mean, noise_std, size = symbols.shape)
  return noise + symbols
