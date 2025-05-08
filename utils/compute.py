import numpy as np
from scipy.stats import pearsonr 

def _present_sbox_output_nibble(plaintexts, keys, nibble_idx, PRESENT_SBOX):
    
    pt_nib = plaintexts[:, nibble_idx] & 0x0F
    key_nib = keys[:, nibble_idx] & 0x0F

    sbox_input = pt_nib ^ key_nib
    return PRESENT_SBOX[sbox_input]


def _present_sbox_outputs(plaintexts, keys, sbox):
    n_traces = plaintexts.shape[0]
    sbox_outputs = np.zeros((n_traces, 16), dtype=np.uint8)

    for i in range(16): # For each nibble
        sbox_outputs[:, i] = _present_sbox_output_nibble(plaintexts, keys, nibble_idx=i, PRESENT_SBOX=sbox)
    return sbox_outputs


def _aes_sbox_output_byte(plaintexts, keys, byte, AES_SBOX):
    pt_bytes = plaintexts[:, byte]
    key_bytes = keys[:, byte]
    xor_bytes = np.bitwise_xor(pt_bytes, key_bytes)
    return AES_SBOX[xor_bytes]


def _aes_sbox_outputs(plaintexts, keys, sbox):
    xor_bytes = np.bitwise_xor(plaintexts, keys)
    return sbox[xor_bytes]


def _snr(traces, labels, num_classes=256):
    """Compute SNR for each time sample based on label groups (0-255)."""

    class_traces = [[] for _ in range(num_classes)]
    for i, label in enumerate(labels):
        class_traces[label].append(traces[i])
    
    class_traces = [np.array(t) for t in class_traces if len(t) > 0]
    means = np.array([np.mean(c, axis=0) for c in class_traces])
    vars_ = np.array([np.var(c, axis=0) for c in class_traces])
    
    mean_global = np.mean(means, axis=0)
    var_between = np.var(means, axis=0)
    var_within = np.mean(vars_, axis=0)
    
    snr = var_between / (var_within + 1e-9)  # Epsilon to avoid division by zero
    return snr


def _correlation(traces, labels):
    """
    Compute the absolute Pearson correlation between trace samples and Hamming weight of labels.
    """
    def hamming_weight(x):
        return bin(x).count('1')
    leakage = np.array([hamming_weight(v) for v in labels])
    correlations = []
    for t in range(traces.shape[1]):
        corr, _ = pearsonr(traces[:, t], leakage)
        correlations.append(abs(corr))
    return np.array(correlations)