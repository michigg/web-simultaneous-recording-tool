import numpy as np


# From: https://librosa.org/doc/main/_modules/librosa/core/convert.html#A_weighting
# Used directly because librosa package installation fails
def A_weighting(frequencies, min_db=-80.0):  # pylint: disable=invalid-name
    """Compute the A-weighting of a set of frequencies.

    Parameters
    ----------
    frequencies : scalar or np.ndarray [shape=(n,)]
        One or more frequencies (in Hz)

    min_db : float [scalar] or None
        Clip weights below this threshold.
        If `None`, no clipping is performed.

    Returns
    -------
    A_weighting : scalar or np.ndarray [shape=(n,)]
        ``A_weighting[i]`` is the A-weighting of ``frequencies[i]``
    """
    f_sq = np.asanyarray(frequencies) ** 2.0

    const = np.array([12200, 20.6, 107.7, 737.9]) ** 2.0
    weights = 2.0 + 20.0 * (
            np.log10(const[0])
            + 2 * np.log10(f_sq)
            - np.log10(f_sq + const[0])
            - np.log10(f_sq + const[1])
            - 0.5 * np.log10(f_sq + const[2])
            - 0.5 * np.log10(f_sq + const[3])
    )

    return weights if min_db is None else np.maximum(min_db, weights)
