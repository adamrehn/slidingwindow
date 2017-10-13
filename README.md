Sliding Window
==============

This is a simple little Python library for computing a set of windows into a larger dataset, designed for use with image-processing algorithms that utilise a sliding window to break the processing up into a series of smaller chunks. In addition, a set of optional transformations can be specified to be applied to each window.

Functionality is also included to compute a distance matrix for a window, for use cases where the position of each pixel in a window (relative to its centre) needs to be taken into account.


Installation
------------

To install, run:

```
pip install slidingwindow
```


Usage Example
-------------

```
import slidingwindow as sw
import numpy as np

# Load our input image here
# data = load(...)

# Generate the set of windows, with a 256-pixel max window size and 50% overlap
windows = sw.generate(data, sw.DimOrder.HeightWidthChannel, 256, 0.5)

# Do stuff with the generated windows
for window in windows:
	subset = data[ window.indices() ]
	# ...

# Or, using some transformation functions
tranforms = [
	lambda m: np.fliplr(m),
	lambda m: np.flipud(m),
	lambda m: np.rot90(m, k=1, axes=(0, 1)),
	lambda m: np.rot90(m, k=3, axes=(0, 1))
]
windows = sw.generate(data, sw.DimOrder.HeightWidthChannel, 256, 0.5, tranforms)
for window in windows:
	transformed = window.apply(data)
	# ...

```
