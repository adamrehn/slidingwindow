import numpy as np

def cropRect(rect, cropTop, cropBottom, cropLeft, cropRight):
	"""
	Crops a rectangle by the specified number of pixels on each side.
	
	The input rectangle and return value are both a tuple of (x,y,w,h).
	"""
	
	# Unpack the rectangle
	x, y, w, h = rect
	
	# Crop by the specified value
	x += cropLeft
	y += cropTop
	w -= (cropLeft + cropRight)
	h -= (cropTop + cropBottom)
	
	# Re-pack the padded rect
	return (x,y,w,h)


def padRect(rect, padTop, padBottom, padLeft, padRight, bounds):
	"""
	Pads a rectangle by the specified values on each individual side,
	ensuring the padded rectangle falls within the specified bounds.
	
	The input rectangle, bounds, and return value are all a tuple of (x,y,w,h).
	"""
	
	# Unpack the rectangle
	x, y, w, h = rect
	
	# Pad by the specified value
	x -= padLeft
	y -= padTop
	w += (padLeft + padRight)
	h += (padTop + padBottom)
	
	# Clip any underflows
	x = max(0, x)
	y = max(0, y)
	
	# Clip any overflows
	overflowY = (y + h) - bounds[0]
	overflowX = (x + w) - bounds[1]
	h -= overflowY if overflowY > 0 else 0
	w -= overflowX if overflowX > 0 else 0
	
	# Re-pack the padded rect
	return (x,y,w,h)


def padRectEqually(rect, padding, bounds):
	"""
	Applies equal padding to all sides of a rectangle,
	ensuring the padded rectangle falls within the specified bounds.
	
	The input rectangle, bounds, and return value are all a tuple of (x,y,w,h).
	"""
	return padRect(rect, padding, padding, padding, padding, bounds)


def squareAspect(rect):
	"""
	Crops either the width or height, as necessary, to make a rectangle into a square.
	
	The input rectangle and return value are both a tuple of (x,y,w,h).
	"""
	
	# Determine which dimension needs to be cropped
	x,y,w,h = rect
	if w > h:
		cropX = (w - h) // 2
		return cropRect(rect, 0, 0, cropX, cropX)
	elif w < h:
		cropY = (h - w) // 2
		return cropRect(rect, cropY, cropY, 0, 0)
	
	# Already a square
	return rect
