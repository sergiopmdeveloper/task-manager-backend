from typing import Dict, NewType, Union

from bson import ObjectId


FakeFindOneResponse = NewType("FakeFindOneResponse", Dict[str, Union[str, ObjectId]])
