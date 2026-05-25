from dataclasses import dataclass
from enum import Enum


class Status(str, Enum):
    WORKING = "working"
    BROKEN  = "broken"
    REPAIR  = "repair"
    RETIRED = "retired"



@dataclass
class Device:
    pc_id:  str
    status: Status
    room:   str

    def __post_init__(self):
        if not self.pc_id.strip():
            raise ValueError("pc_id бос болмауы керек!")
        if not isinstance(self.status, Status):
            self.status = Status(self.status)
        if not self.room.strip():
            raise ValueError("room бос болмауы керек!")

    def is_ok(self):
        return self.status == Status.WORKING

    def to_dict(self):
        return {"pc_id": self.pc_id, "status": self.status.value, "room": self.room}



if __name__ == "__main__":


   
    try:
        dev1 = Device(pc_id="PC-101-01", status="working", room="101")
        print(f"Құрылғы сәтті құрылды: {dev1.pc_id}, Күйі: {dev1.status.value}, Жарамды: {dev1.is_ok()}")
    except ValueError as e:
        print(f"Қате: {e}")

   
    try:
        dev2 = Device(pc_id="   ", status="broken", room="102")
    except ValueError as e:
        print(f"Күтілген қате (pc_id бос): {e}")

    
    try:
        dev3 = Device(pc_id="PC-102-05", status="repair", room="")
    except ValueError as e:
        print(f"Күтілген қате (room бос): {e}")
