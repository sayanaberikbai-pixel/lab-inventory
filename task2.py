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
            self.status = Status(self.status)  # "working" (str) -> Status.WORKING (Enum)
        if not self.room.strip():
            raise ValueError("room бос болмауы керек!")

    def is_ok(self):
        return self.status == Status.WORKING

    def to_dict(self):
        return {"pc_id": self.pc_id, "status": self.status.value, "room": self.room}



class LabInventory:
    def __init__(self, name="Computer Lab"):
        self.name = name
        self._db: dict[str, Device] = {}

    def add(self, device: Device):
        if device.pc_id in self._db:
            raise KeyError(f"{device.pc_id} бұрыннан бар!")
        self._db[device.pc_id] = device

    def update(self, pc_id: str, new_status):
        self._db[pc_id].status = Status(new_status) if isinstance(new_status, str) else new_status

    def remove(self, pc_id: str):
        return self._db.pop(pc_id)

    def all(self):
        return list(self._db.values())

    def by_status(self, s):
        s = Status(s) if isinstance(s, str) else s
        return [d for d in self._db.values() if d.status == s]

    def by_room(self, room):
        return [d for d in self._db.values() if d.room == room]

    def counts(self):
        c = {s.value: 0 for s in Status}
        for d in self._db.values():
            c[d.status.value] += 1
        return c

    def summary(self):
        c = self.counts()
        total = len(self._db)
        rate  = sum(1 for d in self._db.values() if d.is_ok()) / total * 100 if total else 0
        print(f"\n{self.name} | Total: {total} | Working rate: {rate:.1f}%")
        for s, n in c.items():
            print(f"  {s}: {n}")



if __name__ == "__main__":

    inv = LabInventory("Бас Ғимарат Сыныбы")


    inv.add(Device("PC-101", "working", "101"))
    inv.add(Device("PC-102", "repair", "101"))
    inv.add(Device("PC-103", "working", "102"))
    inv.add(Device("PC-104", "broken", "102"))


    inv.update("PC-101", "repair")
    print(f"PC-101 жаңа күйі: {inv._db['PC-101'].status.value}")


    repair_devices = inv.by_status("repair")
    print(f"Жөндеудегі құрылғылар саны: {len(repair_devices)}")


    inv.summary()


    inv.remove("PC-104")
    print(f"Өшірілгеннен кейінгі жалпы саны: {len(inv.all())}")