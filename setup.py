from distutils.core import setup
import py2exe

class Target:
	def __init__(self, **kw):
		self.__dict__.update(kw)
		# for the versioninfo resources
		self.version = '1.0'
		self.company_name = 'jhakonen.com'
		self.copyright = 'no copyright'
		self.name = 'Combileike'
		self.description = 'Combined clipboard for Vista/Win7 and Linux.'

windows_target = Target(
	script = 'application.py',
	dest_base = 'Combileike',
)

setup(
	options = {
		'py2exe': {
			'excludes': ["gtk"],
			'compressed': 1,
			'optimize': 2,
			'bundle_files': 1,
			'dll_excludes': ['w9xpopen.exe']
		}
	},
	windows = [windows_target],
	zipfile = None
)
