# __init__.py

import pathlib
import tomli
import tomli_w

class Setup():
	def __init__(self):
		self.path = pathlib.Path(__file__).parent / "setup.toml"

	def get(self):
		with self.path.open(mode = "rb") as fp:
			config = tomli.load(fp)
		return config

	def set(self, value):
		with self.path.open(mode="wb") as fp:
			tomli_w.dump(value, fp)