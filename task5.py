from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, jsonify

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

class LabInventoryTask5:
    def __init__(self, name="Computer Lab"):
        self.name = name
        self._db: dict[str, Device] = {}

    def add(self, device: Device):
        self._db[device.pc_id] = device

    def by_room(self, room):
        return [d for d in self._db.values() if d.room == room]

    def all(self):
        return list(self._db.values())

    def counts(self):
        c = {s.value: 0 for s in Status}
        for d in self._db.values():
            c[d.status.value] += 1
        return c

    def room_table(self):
        df = pd.DataFrame([d.to_dict() for d in self._db.values()])
        if df.empty:
            return pd.DataFrame()
        g = df.groupby(["room", "status"]).size().reset_index(name="count")
        p = g.pivot_table(index="room", columns="status", values="count", fill_value=0)
        p["total"] = p.sum(axis=1)
        return p

    def plot(self, path="reports/bar.png"):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        c = self.counts()
        colors = {"working": "#4CAF50", "repair": "#FF9800", "broken": "#F44336", "retired": "#9E9E9E"}
        fig, ax = plt.subplots(figsize=(7, 4))
        bars = ax.barh(list(c.keys()), list(c.values()), color=[colors.get(k, "#9E9E9E") for k in c])
        ax.bar_label(bars, padding=4, fontweight="bold")
        ax.set_title(f"{self.name} - Status Distribution", fontweight="bold")
        ax.spines[["top", "right"]].set_visible(False)
        plt.tight_layout()
        fig.savefig(path, dpi=150)
        plt.close()

    def api(self):
        app = Flask(__name__)
        inv = self

        @app.get("/api/report")
        def report():
            return jsonify(inv.room_table().reset_index().to_dict(orient="records"))

        @app.get("/api/report/<room>")
        def room_report(room):
            devs = inv.by_room(room)
            if not devs:
                return jsonify({"error": "not found"}), 404
            return jsonify({"room": room, "total": len(devs), "devices": [d.to_dict() for d in devs]})

        @app.get("/api/devices")
        def devices():
            return jsonify([d.to_dict() for d in inv.all()])

        @app.get("/api/counts")
        def counts():
            return jsonify(inv.counts())

        return app

if __name__ == "__main__":

    inv = LabInventoryTask5("API Желілік Сыныбы")
    inv.add(Device("PC-A", "working", "301"))
    inv.add(Device("PC-B", "repair", "301"))
    inv.add(Device("PC-C", "retired", "302"))

    inv.plot("reports/status_chart.png")
    print("Диаграмма суреті 'reports/status_chart.png' жолына сақталды.")

    app = inv.api()
    app.config["TESTING"] = True
    with app.test_client() as client:
        res_counts = client.get('/api/counts')
        print(f"API /api/counts деректері: {res_counts.get_json()}")
        res_report = client.get('/api/report')
        print(f"API /api/report деректері: {res_report.get_json()}")