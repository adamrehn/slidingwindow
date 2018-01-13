import mmap, tempfile
import numpy as np

class TempfileBackedArray(np.ndarray):
	"""
	A NumPy ndarray that uses a memory-mapped temp file as its backing 
	"""
	
	def __new__(subtype, shape, dtype=float, buffer=None, offset=0, strides=None, order=None, info=None):
		
		# Determine the size in bytes required to hold the array
		size = 1
		for k in shape:
			size *= k
		numBytes = size * np.dtype(dtype).itemsize
		
		# Create the temporary file, resize it, and map it into memory
		tempFile = tempfile.TemporaryFile()
		tempFile.truncate(numBytes)
		buf = mmap.mmap(tempFile.fileno(), numBytes, access=mmap.ACCESS_WRITE)
		
		# Create the ndarray with the memory map as the underlying buffer
		obj = super(TempfileBackedArray, subtype).__new__(subtype, shape, dtype, buffer, offset, strides, order)
		
		# Attach the file reference to the ndarray object
		obj._file = tempFile
		return obj
	
	def __array_finalize__(self, obj):
		if obj is None: return
		self._file = getattr(obj, '_file', None)


def arrayFactory(shape, dtype=float):
	"""
	Creates a new ndarray of the specified shape and datatype, storing
	it in memory if there is sufficient available space or else using
	a memory-mapped temporary file to provide the underlying buffer.
	"""
	try:
		return np.ndarray(shape=shape, dtype=dtype)
	except MemoryError:
		return TempfileBackedArray(shape=shape, dtype=dtype)


def zerosFactory(shape, dtype=float):
	"""
	Creates a new NumPy array using `arrayFactory()` and fills it with zeros.
	"""
	arr = arrayFactory(shape=shape, dtype=dtype)
	arr.fill(0)
	return arr
