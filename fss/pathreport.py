from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class PathValidationError:
	path: Path
	message: str

@dataclass
class PathReport:
	errors_by_path: dict[Path, list[str]]

	def has_error(self):

		for errors in self.errors_by_path.values():
			if(len(errors) > 0):
				return True

		return False

	def get_errors(self, path: Path) -> Optional[list[str]]:
		return self.errors_by_path.get(path, None)

	def add_error(self, path: Path, error: str):

		# init value if doesn't exists
		self.errors_by_path[path] = self.errors_by_path.get(path, [])

		# add error to the path
		self.errors_by_path[path].append(error)
