from setuptools import setup

setup(
	name = 'slidingwindow',
	version = '0.0.9',
	description = 'Sliding Window library for image processing in Python',
	url = 'https://github.com/adamrehn/slidingwindow',
	author = 'Adam Rehn',
	author_email = 'adam@adamrehn.com',
	license = 'MIT',
	packages = ['slidingwindow'],
	zip_safe = True,
	install_requires = [
		'numpy'
	]
)
