from typing import Dict, List, Union

JSON = Union[str, int, float, None, bool, List["JSON"], Dict[str, "JSON"]]
