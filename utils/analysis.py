from collections import defaultdict
import numpy as np
from .compute import _snr, _correlation, _present_sbox_output_nibble

def analyze_leakage_all_nibbles(traces, plaintexts, keys, sbox, top_k=3, is_nibble_level=False):
    """
    Analyze leakage for all 16 key nibbles (AES) or 16 nibbles (PRESENT).

    Parameters:
        traces (np.ndarray): trace array (n_traces x time_samples)
        plaintexts (np.ndarray): shape (n_traces, 8 or 16)
        keys (np.ndarray): same shape as plaintexts
        sbox (np.ndarray): the SBox array to use (AES or PRESENT)
        top_k (int): number of POIs to report
        is_nibble_level (bool): True for PRESENT (nibble), False for AES (byte)

    Returns:
        nibble_results: dict of results per nibble/nibble index
    """
    nibble_results = defaultdict(dict)
    total_units = 16  # 16 bytes (AES) or 16 nibbles (PRESENT)

    for idx in range(total_units):
        print(f"\n Analyzing {'nibble' if is_nibble_level else 'byte'} {idx}...")

        sbox_output = _present_sbox_output_nibble(plaintexts, keys, nibble_idx=idx, PRESENT_SBOX=sbox)
        # Compute SNR
        snr = _snr(traces, sbox_output)
        nibble_results[idx]['snr'] = snr

        # Compute correlation
        corr = _correlation(traces, sbox_output)
        nibble_results[idx]['correlation'] = corr

        # Print top leakage time samples
        top_snr = np.argsort(snr)[-top_k:][::-1]
        top_corr = np.argsort(corr)[-top_k:][::-1]
        print(f"  Top SNR POIs: {top_snr}, values: {snr[top_snr]}")
        print(f"  Top Corr POIs: {top_corr}, values: {corr[top_corr]}")

    return nibble_results
