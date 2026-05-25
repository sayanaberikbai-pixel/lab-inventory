from dataclasses import dataclass
from enum import Enum
import pandas as pd

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

    def to_dict(self):
        return {"pc_id": self.pc_id, "status": self.status.value, "room": self.room}

class LabInventoryTask4:
    def __init__(self):
        self._db: dict[str, Device] = {}

    def add(self, device: Device):
        self._db[device.pc_id] = device

    def to_df(self):
        return pd.DataFrame([d.to_dict() for d in self._db.values()])

    def grouped(self):
        return self.to_df().groupby(["room", "status"]).size().reset_index(name="count")

    def pivot(self):
        return self.grouped().pivot_table(index="room", columns="status", values="count", fill_value=0)

    def room_table(self):
        p = self.pivot()
        p["total"] = p.sum(axis=1)
        if "working" in p.columns:
            p["ok_%"] = (p["working"] / p["total"] * 100).round(1)
        return p

if __name__ == "__main__":

    inv = LabInventoryTask4()
    inv.add(Device("PC-1", "working", "101"))
    inv.add(Device("PC-2", "broken", "101"))
    inv.add(Device("PC-3", "working", "101"))
    inv.add(Device("PC-4", "repair", "102"))
    inv.add(Device("PC-5", "working", "102"))

    print("Бөлме мен күй бойынша топтау (Grouped):")
    print(inv.grouped().to_string(index=False))

    print("\nАудиториялар бойынша толық есеп (Pivot + Қорытынды):")
    print(inv.room_table())