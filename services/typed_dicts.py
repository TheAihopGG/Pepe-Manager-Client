from typing import TypedDict

__doc__ = """Contains TypedDicts"""

class TypedPackage(TypedDict):
    id: int
    name: str
    author: str
    version: str
    url: str


class TypedConfig(TypedDict):
    packages_dir_path: str
    packages: list[TypedPackage]
