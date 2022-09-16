import enum
import json


class CommandState(enum.Enum):
    COMPLETED = "completed"
    ERROR = "error"


class CommandRequest:
    @classmethod
    def unmarshal_json(cls, data):
        req = json.loads(data)
        return cls(id_=req["id"], name=req["name"], args=req.get("arguments"))

    def __init__(self, id_, name, args=None):
        self.id = id_
        self.name = name

        if args is None:
            args = {}
        self.args = args

    def new_response(self, *args, **kwargs):
        return CommandResponse(self.id, *args, **kwargs)


class CommandResponse:
    def __init__(self, id_, state, payload=None):
        self.id = id_

        if not isinstance(state, CommandState):
            state = CommandState(state)
        self.state = state

        if not isinstance(payload, dict):
            payload = {"message": payload}
        self.payload = payload

    def json(self):
        json_object = {"id": self.id, "state": self.state.value}
        if self.payload is not None:
            json_object["payload"] = self.payload

        return json_object
