"""
Miscellaneous helper functions

author: William Tong (wlt2115@columbia.edu)
date: February 12, 2019
"""

import logging

import numpy as np

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
                domain: np.ndarray,
                energy_range: tuple,
                max_iterations: int = 10000,
                check_every: int = 1000,
                update_every: int = 500,
                flatness: float = 0.95,
                resolution: int = 10,
                step_size: float = 1) -> 'dict':

    e_min, e_max = energy_range
    e_spectrum = np.arange(e_min, e_max, 1 / resolution)

    S = {e: 0 for e in e_spectrum}
    H = {e: 0 for e in e_spectrum} # TODO: need to generalize to higher dims
    g = lambda loc: _propose(loc, step_size, domain)
    f = 1

    def E(x: float) -> float:
        raw_energy = energy(x)
        buckets = list(S.keys())
        min_idx = np.argmin([np.abs(buckets[i] - raw_energy)
                             for i in range(len(buckets))]) # TODO: in much need of optimization (bisect-left)
        return buckets[min_idx]

    def _accept(r: float, r_prime: float) -> bool:
        ratio = np.e ** (S[E(r)] - S[E(r_prime)])
        do_accept = np.random.rand() <= ratio
        return do_accept

    r = [_rand_float(*bound) for bound in domain]
    for iteration in range(1, max_iterations):
        r_prime = g(r)
        if _accept(r, r_prime):
            r = r_prime

        E_i = E(r)
        H[E_i] += 1
        S[E_i] += f

        if iteration % check_every == 0:
            if _is_flat(H, flatness):
                break

        if iteration % update_every == 0:
            f /= 2  # TODO: change to be proportional to 1/t
            logging.info("Iteration %d f=%f" % (iteration, f))

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

    return min >= flatness_ratio * mean


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    peaks = [1, 5, 10]
    locs = np.array([[-5], [0], [5]])

    f = shekel(peaks, locs)
    x = np.arange(-10, 10, 0.01)
    plt.plot(x, [f(i) for i in x])
    plt.show()





