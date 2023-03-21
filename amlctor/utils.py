from importlib.util import spec_from_file_location
from pathlib import Path


	
def get_settingspy_module(path: Path) -> dict:
		""" 
				returns names from the `settings.py` modul of the pipeline `path` directory 
				path:           pipeline path
				returns:        dict of names from the module. 
		"""
		path_settingspy = str(path / 'settings.py')
		spec = spec_from_file_location('settings', path_settingspy)
		dirs = dir(spec.loader.load_module())
		dirs = [dir for dir in dirs if  not dir.startswith('__') and dir.endswith('__')]
		kws = {}
		module = spec.loader.load_module()
		for kw in dirs:
				kws[kw] = module.__dict__[kw]

		return kws



def is_pipe(path: Path, pipe_name: str = None, is_step: bool = False) -> bool:
		""" 
			Returns True if directory is pipeline. 
			Actually, checks if directory contains `files_to_check`.
			`pipe_name`:	if passed checks if name is exactly passed one
			`is_step`:		if True, pipe_name should be step_name
		"""
		contains_pipe = None
		# check if there is any pipe
		if path / 'settings' in path.iterdir():   # has settings dir
			settings_path = path / 'settings'
			files_to_check = ('.env', 'conda_dependencies.yml', 'settings.py')
			for file in files_to_check:
				if not file in settings_path.iterdir():
					return False
				
			contains_pipe = True
		
		else:
			return False	# there is no any pipeline
		
		if pipe_name is None:
			return contains_pipe  # has an pipe and it's enough
		
		else:
			settingspy = get_settingspy_module(path)					# we have the name for checking
			if not isinstance(pipe_name, str):
				raise ValueError(f"Incorrect pipeline name '{pipe_name}' type: '{type(pipe_name)}'")
			
			if is_step is False:	# name is pipeline name
				return settingspy['NAME'] == pipe_name

			elif is_step is True:
				for step in settingspy['STEPS']:
					if pipe_name == step.name:
						return True		# step name found
				return False			# not fount
			else:
				raise ValueError(f"'is_step' should be boolean not '{type(is_step)}'")

		
		 


