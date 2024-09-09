from dataclasses import asdict, dataclass, fields
from typing import Any, Optional


@dataclass
class DTO:
    def as_dict(self, exclude_none: bool = False) -> dict:
        if exclude_none:
            return asdict(self, dict_factory=lambda field: {key: value for (key, value) in field if value is not None})
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict, **kwargs) -> Any:
        field_names = [field.name for field in fields(cls)]
        filtered_fields = {}

        data.update(kwargs)

        for key, value in data.items():
            if key in field_names:
                filtered_fields[key] = value

        return cls(**filtered_fields)  # type: ignore

    @classmethod
    def model_to_dto(cls, from_model_dt_class: dataclass, **kwargs):
        from_dt_dict = asdict(from_model_dt_class)
        return cls.from_dict(from_dt_dict, **kwargs)
