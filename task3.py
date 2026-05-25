import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

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

class LabInventoryTask3:
    def __init__(self, name="Computer Lab"):
        self.name = name
        self._db: dict[str, Device] = {}

    def add(self, device: Device):
        self._db[device.pc_id] = device

    def all(self):
        return list(self._db.values())

    def broken_gen(self):
        for d in self._db.values():
            if d.status in (Status.BROKEN, Status.REPAIR):
                yield d

    def to_json(self, path="data/inv.json"):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps({"lab": self.name, "devices": [d.to_dict() for d in self._db.values()]},
                       ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    @classmethod
    def from_json(cls, path="data/inv.json"):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        inv  = cls(data["lab"])
        for item in data["devices"]:
            inv._db[item["pc_id"]] = Device(**item)
        return inv

if __name__ == "__main__":

    inv = LabInventoryTask3("Экспорт Орталығы")
    inv.add(Device("PC-201", "broken", "201"))
    inv.add(Device("PC-202", "working", "201"))
    inv.add(Device("PC-203", "repair", "202"))

    print("Ақаулы құрылғылар тізімі (Генератор):")
    for dev in inv.broken_gen():
        print(f"  ID: {dev.pc_id} | Күйі: {dev.status.value}")

    inv.to_json("test_data/inventory.json")
    print("Деректер test_data/inventory.json файлына жазылды.")

    loaded_inv = LabInventoryTask3.from_json("test_data/inventory.json")
    print(f"Файлдан жүктелген құрылғылар саны: {len(loaded_inv.all())}")