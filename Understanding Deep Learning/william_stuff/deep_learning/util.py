"""
Miscellaneous helper functions

author: William Tong (wlt2115@columbia.edu)
date: February 12, 2019
"""

import logging
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO)


def shekel(peaks: np.ndarray, locs: np.ndarray, negate=False) -> 'function':
    """
    Generates a shekel function with the given peaks at the specified locations.
    The dimensionality is based on the number of coordinates per location
    in the locs array. For example, if two coordinates x and y are specified
    per each peak, the resulting shekel function will be three dimensional.

    :param peaks: np.array of magnitudes of peaks
    :param locs: location for each peak
    :param negate: if True, will turn all peaks into valleys
    :return: shekel function. Call as you would any function: e.g. func(x)
    """

    if type(peaks) is not np.ndarray:
        peaks = np.array(peaks)
    if type(locs) is not np.ndarray:
        locs = np.array(locs)

    if not len(peaks.shape) == 1:
        raise TypeError('Argument "peaks" should be single-dimensional')
    if not len(locs.shape) == 2:
        raise TypeError('Argument "locs" should be two-dimensional')

    num_peaks = peaks.shape[0]
    num_dims = locs.shape[1]
    if not locs.shape == (num_peaks, num_dims):
        raise TypeError("Expected locs dim to be: %s, received %s"
                        % ((num_peaks, num_dims), locs.shape))

    c = 1 / peaks
    a = -locs

    def f(x):
        if not isinstance(x, list):
            x = [x]

        out_sum = 0
        for i in range(len(c)):
            in_sum = 0
            for j in range(len(x)):
                in_sum += (x[j] - a[i][j]) ** 2

            out_sum += (in_sum + c[i]) ** -1

        if negate:
            out_sum = -out_sum
        return out_sum

    return f


def wang_landau(energy: 'function',
                domain: np.ndarray,             # Must be (n x 2)
                energy_range: tuple,
                max_iterations: int = 10000,
                final_f: float = 0.001,
                check_every: int = 100,
                save_every: int = 1000,
                log_dir: Path = None,
                flatness: float = 0.90,
                resolution: int = 10,
                step_size: float = 1) -> 'dict':

    snapshot_path = log_dir / 'snapshots.txt'

    if len(energy_range) > 2:
        e_spectrum = energy_range
    else:
        e_min, e_max = energy_range
        e_spectrum = np.arange(e_min, e_max, 1 / resolution)

    S = {e: 0 for e in e_spectrum}
    H = {e: 0 for e in e_spectrum}
    g = lambda loc: _propose(loc, step_size, domain)
    f = 1

    def E(x) -> float:
        raw_energy = energy(x)
        buckets = list(S.keys())
        min_idx = np.argmin([np.abs(buckets[i] - raw_energy)
                             for i in range(len(buckets))]) # TODO: in much need of optimization (bisect-left)
        return buckets[min_idx]

    def _accept(r: float, r_prime: float) -> bool:
        difference = S[E(r)] - S[E(r_prime)]
        if difference >= 0:
            return True

        ratio = np.e ** difference
        do_accept = np.random.rand() <= ratio
        return do_accept

    r = np.array([_rand_float(*bound) for bound in domain])
    for iteration in range(1, max_iterations):
        r_prime = g(r)
        if _accept(r, r_prime):
            r = r_prime

        E_i = E(r)
        H[E_i] += 1
        S[E_i] += f

        if iteration % save_every == 0 \
                and log_dir is not None:
            if not log_dir.exists():
                Path.mkdir(log_dir, parents=True)

            filename = 'wl_iter=%i_f=%f.png' % (iteration, f)
            save_path = log_dir / filename
            _plot_progress(S, H, str(save_path))
            _save_snapshot(S, str(snapshot_path))

        if iteration % check_every == 0:
            logging.info("Iteration %d f=%f" % (iteration, f))

            test_H = {e: H[e] for e in H.keys() if H[e] != 0}  # TODO: set option to disable / tune
            if _is_flat(test_H, flatness):
                logging.info("Histogram flat at iteration %d" % iteration)

                for state in H.keys():
                    H[state] = 0
                f /= 2  # TODO: change to be proportional to 1/t
                if f < final_f:
                    _save_snapshot(S, str(snapshot_path))
                    return S, H

    logging.warning("Exiting before final_f reached. f is: %f" % f)
    _save_snapshot(S, str(snapshot_path)) # TODO: perfect save before end
    return S, H


def _propose(loc: list, scale: float, domain: tuple) -> np.ndarray:
    raw_proposals = np.random.normal(loc, scale)
    proposals = np.array([_wrap(raw_proposals[i], domain[i]) for i in range(len(raw_proposals))])

    return proposals


def _wrap(pos: float, bound: tuple) -> float:
    if pos < bound[0]:
        return bound[1] - np.abs(pos - bound[0])
    elif pos > bound[1]:
        return bound[0] + np.abs(pos - bound[1])
    else:
        return pos


def _rand_float(lower: float, upper: float) -> float:
    return np.random.rand() * (upper - lower) + lower


def _is_flat(histogram: dict, flatness_ratio: float) -> bool:
    values = [histogram[bin] for bin in histogram.keys()]
    mean = np.mean(values)
    min = np.min(values)

    logging.info('At check, min: %f mean: %f' % (min, mean))
    return min >= flatness_ratio * mean


def _plot_progress(freqs, hist, filename):
    bins = list(freqs.keys())
    values = list(freqs.values())

    plt.subplot(131)
    plt.title("ln of energy density")
    plt.hist(bins, weights=values, bins=len(bins), orientation='horizontal')

    plt.subplot(132)
    max_val = max(values)
    norm_values = [np.e ** (value - max_val) for value in values]
    plt.title("Normalized energy densities")
    plt.hist(bins, weights=norm_values, bins=len(bins), orientation='horizontal')

    plt.subplot(133)
    hist_values = list(hist.values())
    plt.title("visited states")
    plt.hist(bins, weights=hist_values, bins=len(bins), orientation='horizontal')

    plt.savefig(str(filename))
    plt.clf()


def _save_snapshot(S: dict, filename: str) -> None:
    with open(filename, 'a') as snapshot_file:
        snapshot_file.write(str(S))
        snapshot_file.write('\n')


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    peaks = [1, 5, 10]
    locs = np.array([[-5], [0], [5]])

    f = shekel(peaks, locs)
    x = np.arange(-10, 10, 0.01)
    plt.plot(x, [f(i) for i in x])
    plt.show()





