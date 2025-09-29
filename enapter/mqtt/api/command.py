import enum
import json
from typing import Any, Dict, Optional, Union


class CommandState(enum.Enum):
    COMPLETED = "completed"
    ERROR = "error"


class CommandRequest:
    @classmethod
    def unmarshal_json(cls, data: Union[str, bytes]) -> "CommandRequest":
        req = json.loads(data)
        return cls(id_=req["id"], name=req["name"], args=req.get("arguments"))

    def __init__(self, id_: str, name: str, args: Optional[Dict[str, Any]] = None):
        self.id = id_
        self.name = name

        if args is None:
            args = {}
        self.args = args

    def new_response(self, *args, **kwargs) -> "CommandResponse":
        return CommandResponse(self.id, *args, **kwargs)


class CommandResponse:
    def __init__(
        self,
        id_: str,
        state: Union[str, CommandState],
        payload: Optional[Union[Dict[str, Any], str]] = None,
    ) -> None:
        self.id = id_

        if not isinstance(state, CommandState):
            state = CommandState(state)
        self.state = state

        if not isinstance(payload, dict):
            payload = {"message": payload}
        self.payload = payload

    def json(self) -> Dict[str, Any]:
        json_object: Dict[str, Any] = {"id": self.id, "state": self.state.value}
        if self.payload is not None:
            json_object["payload"] = self.payload

        return json_object
