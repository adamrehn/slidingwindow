[![Version](https://img.shields.io/pypi/v/slidingwindow.svg)](https://pypi.python.org/pypi/slidingwindow) ![Build Status](https://img.shields.io/travis/com/adamrehn/slidingwindow)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/slidingwindow/badges/downloads.svg)](https://anaconda.org/conda-forge/slidingwindow)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/slidingwindow/badges/version.svg)](https://anaconda.org/conda-forge/slidingwindow)

Sliding Window
==============

This is a simple little Python library for computing a set of windows into a larger dataset, designed for use with image-processing algorithms that utilise a sliding window to break the processing up into a series of smaller chunks. In addition, a set of optional transformations can be specified to be applied to each window.

Functionality is also included to compute a distance matrix for a window, for use cases where the position of each pixel in a window (relative to its centre) needs to be taken into account, as well as functionality for batching windows and merging the results of processing that is applied to windows.

For use cases where window bounds need to be modified after they have been generated, window objects can be converted to and from rectangles represented by a tuple of (x,y,w,h). Functionality for transforming rectangles (padding, cropping, forcing a square aspect ratio, etc.) are also provided.

Functionality is also provided for NumPy array creation that will fallback to using memory-mapped temporary files for the underling array buffers if there is insufficient system memory available, as well as determining the largest square window size that can be used when generating windows.


Installation
------------

To install with pip, run:

```
pip install slidingwindow
```

To install with conda, run:

```
conda install slidingwindow
```


Usage Example
-------------

```python
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

# Alternatively, if we want to modify each window
windows = sw.generate(data, sw.DimOrder.HeightWidthChannel, 256, 0.5)
for window in windows:
	rect = window.getRect()
	transformed = sw.padRectEqually(rect, 100, data.shape)
	window.setRect(transformed)
	# ...

```
