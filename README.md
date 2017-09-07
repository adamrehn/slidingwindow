Sliding Window
==============

This is a simple little Python library for computing a set of windows into a larger dataset, designed for use with image-processing algorithms that utilise a sliding window to break the processing up into a series of smaller chunks.

Functionality is also included to compute a distance matrix for a window, for use cases where the position of each pixel in a window (relative to its centre) needs to be taken into account.


Installation
------------

To install, run:

```
pip install .
```


Usage Example
-------------

```
import slidingwindow as sw

# Load our input image here
# data = load(...)

# Generate the set of windows, with a 256-pixel max window size and 50% overlap
windows = sw.generate(data, sw.DimOrder.HeightWidthChannel, 256, 0.5)

# Do stuff with the generated windows
for window in windows:
	subset = data[ window.indices() ]
	# ...
```
