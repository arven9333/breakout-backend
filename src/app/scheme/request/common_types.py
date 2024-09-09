from typing import Annotated
from pydantic import Field


GreatOneInt = Annotated[int, Field(gt=0)]