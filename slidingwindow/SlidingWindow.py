import math

class DimOrder(object):
	"""
	Represents the order of the dimensions in a dataset's shape.
	"""
	ChannelHeightWidth = ['c', 'h', 'w']
	HeightWidthChannel = ['h', 'w', 'c']


class SlidingWindow(object):
	"""
	Represents a single window into a larger dataset.
	"""
	
	def __init__(self, x, y, w, h, dimOrder, transform = None):
		"""
		Creates a new window with the specified dimensions and transform
		"""
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.dimOrder = dimOrder
		self.transform = transform
	
	def apply(self, matrix):
		"""
		Slices the supplied matrix and applies any transform bound to this window
		"""
		view = matrix[ self.indices() ]
		return self.transform(view) if self.transform != None else view
	
	def getRect(self):
		"""
		Returns the window bounds as a tuple of (x,y,w,h)
		"""
		return (self.x, self.y, self.w, self.h)
	
	def setRect(self, rect):
		"""
		Sets the window bounds from a tuple of (x,y,w,h)
		"""
		self.x, self.y, self.w, self.h = rect
	
	def indices(self, includeChannel=True):
		"""
		Retrieves the indices for this window as a tuple of slices
		"""
		if self.dimOrder == DimOrder.HeightWidthChannel:
			
			# Equivalent to [self.y:self.y+self.h+1, self.x:self.x+self.w+1]
			return (
				slice(self.y, self.y+self.h),
				slice(self.x, self.x+self.w)
			)
			
		elif self.dimOrder == DimOrder.ChannelHeightWidth:
			
			if includeChannel is True:
				
				# Equivalent to [:, self.y:self.y+self.h+1, self.x:self.x+self.w+1]
				return (
					slice(None, None),
					slice(self.y, self.y+self.h),
					slice(self.x, self.x+self.w)
				)
				
			else:
				
				# Equivalent to [self.y:self.y+self.h+1, self.x:self.x+self.w+1]
				return (
					slice(self.y, self.y+self.h),
					slice(self.x, self.x+self.w)
				)
			
		else:
			raise Error('Unsupported order of dimensions: ' + str(self.dimOrder))
		
	def __str__(self):
		return '(' + str(self.x) + ',' + str(self.y) + ',' + str(self.w) + ',' + str(self.h) + ')'
	
	def __repr__(self):
		return self.__str__()


def generate(data, dimOrder, windowShape, overlapPercent, transforms=[], mode='square'):
	"""
    Generates a set of sliding windows for the specified dataset.
    WindowMode has to be one of 'sqaure', 'rectangle' or 'distribute'.
    """
	# Determine the dimensions of the input data
	imgHeight = data.shape[dimOrder.index('h')]
	imgWidth = data.shape[dimOrder.index('w')]
	imgShape = imgHeight, imgWidth

	if mode == 'sqaure':

		if not isinstance(windowShape, int):
			raise Exception("'windowShape' has to be an integer with a single value in 'square' mode.")

		windowShape = (windowShape, windowShape)

	elif mode == 'rectangle':

		if not isinstance(windowShape, tuple) or len(windowShape) != 2:
			raise Exception(
				"'windowShape' has to be a tuple with height and width of sliding window in 'rectangle' mode.")

	elif mode == 'distribute':

		numWindowY, numWindowX = windowShape

		windowSizeY = math.ceil(imgHeight / numWindowY)
		windowSizeX = math.ceil(imgWidth / numWindowX)

		windowShape = windowSizeY, windowSizeX

	# Generate the windows
	return generateForSize(windowShape, imgShape, dimOrder, overlapPercent, transforms)


def generateForSize(windowShape, imgShape, dimOrder, overlapPercent, transforms=[]):
	"""
	Generates a set of sliding windows for a dataset with the specified dimensions and order.
    """

	windowSizeY, windowSizeX = windowShape

	# Compute the window overlap and step size
	windowOverlapX = int(math.floor(windowSizeX * overlapPercent))
	windowOverlapY = int(math.floor(windowSizeY * overlapPercent))
	stepSizeX = windowSizeX - windowOverlapX
	stepSizeY = windowSizeY - windowOverlapY

	# Determine how many windows we will need in order to cover the input data
	imgHeight, imgWidth = imgShape
	lastX = imgWidth - windowSizeX
	lastY = imgHeight - windowSizeY
	xOffsets = list(range(0, lastX + 1, stepSizeX))
	yOffsets = list(range(0, lastY + 1, stepSizeY))

	# Unless the input data dimensions are exact multiples of the step size,
	# we will need one additional row and column of windows to get 100% coverage
	if len(xOffsets) == 0 or xOffsets[-1] != lastX:
		xOffsets.append(lastX)
	if len(yOffsets) == 0 or yOffsets[-1] != lastY:
		yOffsets.append(lastY)

	# Generate the list of windows
	windows = []
	for xOffset in xOffsets:
		for yOffset in yOffsets:
			for transform in [None] + transforms:
				windows.append(SlidingWindow(
					x=xOffset,
					y=yOffset,
					w=windowSizeX,
					h=windowSizeY,
					dimOrder=dimOrder,
					transform=transform
				))

	return windows
