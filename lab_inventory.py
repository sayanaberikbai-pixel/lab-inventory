"""
Компьютерлік сыныптың инвентарлық жүйесі
Computer Lab Inventory Management System
=========================================
Тапсырмалар 1-14 / Tasks 1-14
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Generator, Iterator

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from flask import Flask, jsonify


# ─────────────────────────────────────────────
# Тапсырма 1-3 | Tasks 1-3: Устройства / Devices
# ─────────────────────────────────────────────

class DeviceStatus(str, Enum):
    """Жабдық күйлері / Device status values."""
    WORKING    = "working"       # Жұмыс істейді
    BROKEN     = "broken"        # Ақаулы
    REPAIR     = "repair"        # Жөндеуде
    RETIRED    = "retired"       # Есептен шығарылған


@dataclass
class Device:
    """
    Тапсырма 1-3: Бір жабдықты сипаттайтын деректер класы.
    Task 1-3: Data class describing a single lab device.

    Attributes:
        pc_id  – бірегей идентификатор (unique identifier)
        status – DeviceStatus enum мәні
        room   – аудитория нөмірі (classroom/room number)
    """
    pc_id:  str
    status: DeviceStatus
    room:   str

    # ── Task 2-3: Validation ──────────────────────────────────────────
    def __post_init__(self) -> None:
        if not self.pc_id.strip():
            raise ValueError("pc_id бос болмауы керек / pc_id must not be empty.")
        if not isinstance(self.status, DeviceStatus):
            try:
                self.status = DeviceStatus(self.status)
            except ValueError:
                valid = [s.value for s in DeviceStatus]
                raise ValueError(f"status мәні {valid} ішінен болуы керек.")
        if not self.room.strip():
            raise ValueError("room бос болмауы керек / room must not be empty.")

    def is_operational(self) -> bool:
        """Жабдық жұмыс істей ме? / Is the device operational?"""
        return self.status == DeviceStatus.WORKING

    def to_dict(self) -> dict:
        """Сөздікке айналдыру / Convert to plain dict."""
        return {"pc_id": self.pc_id, "status": self.status.value, "room": self.room}


# ─────────────────────────────────────────────
# Тапсырма 4-6 | Tasks 4-6: LabInventory класы
# ─────────────────────────────────────────────

class LabInventory:
    """
    Тапсырма 4-6: Инвентарлық жүйенің негізгі класы.
    Task 4-6: Core inventory management class.

    Жабдықтарды қосу, жаңарту, сүзу және есептеу
    функционалдығын қамтамасыз етеді.
    """

    def __init__(self, name: str = "Computer Lab") -> None:
        self.name: str = name
        self._devices: dict[str, Device] = {}   # pc_id → Device

    # ── Task 4: CRUD operations ───────────────────────────────────────

    def add_device(self, device: Device) -> None:
        """Жабдықты тізімге қосу / Add a device to the inventory."""
        if device.pc_id in self._devices:
            raise KeyError(f"'{device.pc_id}' бұрыннан бар / already exists.")
        self._devices[device.pc_id] = device

    def update_status(self, pc_id: str, new_status: DeviceStatus | str) -> Device:
        """Жабдық күйін жаңарту / Update a device's status."""
        device = self.get_device(pc_id)
        device.status = DeviceStatus(new_status) if isinstance(new_status, str) else new_status
        return device

    def remove_device(self, pc_id: str) -> Device:
        """Жабдықты тізімнен шығару / Remove a device."""
        if pc_id not in self._devices:
            raise KeyError(f"'{pc_id}' табылмады / not found.")
        return self._devices.pop(pc_id)

    def get_device(self, pc_id: str) -> Device:
        """Жабдықты идентификатор бойынша алу / Get device by pc_id."""
        if pc_id not in self._devices:
            raise KeyError(f"'{pc_id}' табылмады / not found.")
        return self._devices[pc_id]

    # ── Task 5: Filter / Query functions ─────────────────────────────

    def all_devices(self) -> list[Device]:
        """Барлық жабдықтар / All devices."""
        return list(self._devices.values())

    def filter_by_status(self, status: DeviceStatus | str) -> list[Device]:
        """Күй бойынша сүзу / Filter devices by status."""
        s = DeviceStatus(status) if isinstance(status, str) else status
        return [d for d in self._devices.values() if d.status == s]

    def filter_by_room(self, room: str) -> list[Device]:
        """Аудитория бойынша сүзу / Filter devices by room."""
        return [d for d in self._devices.values() if d.room == room]

    def count_by_status(self) -> dict[str, int]:
        """Күй бойынша сан / Count devices per status."""
        counts: dict[str, int] = {s.value: 0 for s in DeviceStatus}
        for d in self._devices.values():
            counts[d.status.value] += 1
        return counts

    def operational_rate(self) -> float:
        """Жұмыс істейтін жабдықтардың үлесі / Fraction of working devices."""
        if not self._devices:
            return 0.0
        working = sum(1 for d in self._devices.values() if d.is_operational())
        return working / len(self._devices)

    # ── Task 6: Summary ───────────────────────────────────────────────

    def summary(self) -> str:
        """Инвентарь туралы қысқаша мәліметтер / Brief inventory summary."""
        total = len(self._devices)
        counts = self.count_by_status()
        rate = self.operational_rate() * 100
        lines = [
            f"=== {self.name} ===",
            f"Барлығы / Total: {total}",
        ]
        for status, cnt in counts.items():
            lines.append(f"  {status}: {cnt}")
        lines.append(f"Жұмысқа жарамдылық / Operational rate: {rate:.1f}%")
        return "\n".join(lines)

    # ── Task 7: Generator for broken devices ─────────────────────────

    def broken_devices(self) -> Generator[Device, None, None]:
        """
        Тапсырма 7: Ақаулы жабдықтар генераторы.
        Task 7: Generator that yields broken/repair devices one by one.
        """
        for device in self._devices.values():
            if device.status in (DeviceStatus.BROKEN, DeviceStatus.REPAIR):
                yield device

    # ── Task 8: JSON serialization ────────────────────────────────────

    def to_json(self, filepath: str | Path) -> Path:
        """
        Тапсырма 8: Инвентарьды JSON файлына сериализациялау.
        Task 8: Serialize the entire inventory to a JSON file.
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "lab_name": self.name,
            "devices": [d.to_dict() for d in self._devices.values()],
        }
        filepath.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return filepath

    @classmethod
    def from_json(cls, filepath: str | Path) -> "LabInventory":
        """
        Тапсырма 8: JSON файлынан инвентарьды жүктеу.
        Task 8: Deserialize inventory from a JSON file.
        """
        filepath = Path(filepath)
        data = json.loads(filepath.read_text(encoding="utf-8"))
        inv = cls(name=data.get("lab_name", "Lab"))
        for item in data["devices"]:
            inv.add_device(Device(**item))
        return inv

    # ── Task 9-12: Pandas analytics ───────────────────────────────────

    def to_dataframe(self) -> pd.DataFrame:
        """
        Тапсырма 9: Device тізімін DataFrame-ге айналдыру.
        Task 9: Convert devices to a Pandas DataFrame.
        """
        rows = [d.to_dict() for d in self._devices.values()]
        return pd.DataFrame(rows, columns=["pc_id", "status", "room"])

    def groupby_room_status(self) -> pd.DataFrame:
        """
        Тапсырма 9-10: Аудитория және күй бойынша топтастыру.
        Task 9-10: Group by (room, status) and count devices.
        """
        df = self.to_dataframe()
        grouped = (
            df.groupby(["room", "status"])
              .size()
              .reset_index(name="count")
              .sort_values(["room", "status"])
        )
        return grouped

    def pivot_table(self) -> pd.DataFrame:
        """
        Тапсырма 11: Pivot кесте – аудитория × күй.
        Task 11: Pivot table – rows=room, columns=status, values=count.
        """
        grouped = self.groupby_room_status()
        pivot = grouped.pivot_table(
            index="room",
            columns="status",
            values="count",
            fill_value=0,
            aggfunc="sum",
        )
        pivot.columns.name = None
        return pivot

    def room_summary_table(self) -> pd.DataFrame:
        """
        Тапсырма 12: Аудитория бойынша қорытынды кесте.
        Task 12: Room-level summary with total and operational rate.
        """
        pivot = self.pivot_table()
        pivot["total"] = pivot.sum(axis=1)
        working_col = DeviceStatus.WORKING.value
        if working_col in pivot.columns:
            pivot["operational_%"] = (pivot[working_col] / pivot["total"] * 100).round(1)
        else:
            pivot["operational_%"] = 0.0
        return pivot

    # ── Task 13: Bar chart ────────────────────────────────────────────

    def plot_status_bar(self, save_path: str | Path = "reports/status_bar.png") -> Path:
        """
        Тапсырма 13: Күй бойынша bar-диаграмма.
        Task 13: Horizontal bar chart of device counts per status.
        """
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        counts = self.count_by_status()
        statuses = list(counts.keys())
        values   = list(counts.values())

        colors = {
            "working": "#4CAF50",
            "repair":  "#FF9800",
            "broken":  "#F44336",
            "retired": "#9E9E9E",
        }
        bar_colors = [colors.get(s, "#607D8B") for s in statuses]

        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.barh(statuses, values, color=bar_colors, edgecolor="white", height=0.6)
        ax.bar_label(bars, padding=4, fontsize=11, fontweight="bold")
        ax.set_xlabel("Жабдықтар саны / Number of Devices", fontsize=11)
        ax.set_title(f"{self.name} — Күй бойынша / By Status", fontsize=13, fontweight="bold", pad=14)
        ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="x", linestyle="--", alpha=0.5)
        plt.tight_layout()
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return save_path

    # ── Task 14: Flask REST API ───────────────────────────────────────

    def create_flask_app(self) -> Flask:
        """
        Тапсырма 14: Аудитория бойынша есеп REST API.
        Task 14: Flask REST API for room-level reports.

        Маршруттар / Endpoints:
            GET /api/report           – барлық аудитория есебі
            GET /api/report/<room>    – бір аудитория есебі
            GET /api/devices          – барлық жабдықтар тізімі
            GET /api/status_counts    – күй бойынша санақ
        """
        app = Flask(__name__)
        inventory = self   # closure reference

        @app.get("/api/report")
        def full_report():
            table = inventory.room_summary_table()
            result = table.reset_index().to_dict(orient="records")
            return jsonify({"lab": inventory.name, "rooms": result})

        @app.get("/api/report/<room>")
        def room_report(room: str):
            devices = inventory.filter_by_room(room)
            if not devices:
                return jsonify({"error": f"Room '{room}' not found"}), 404
            counts: dict[str, int] = {s.value: 0 for s in DeviceStatus}
            for d in devices:
                counts[d.status.value] += 1
            total = len(devices)
            working = counts.get(DeviceStatus.WORKING.value, 0)
            return jsonify({
                "room": room,
                "total": total,
                "counts": counts,
                "operational_%": round(working / total * 100, 1) if total else 0,
                "devices": [d.to_dict() for d in devices],
            })

        @app.get("/api/devices")
        def list_devices():
            return jsonify([d.to_dict() for d in inventory.all_devices()])

        @app.get("/api/status_counts")
        def status_counts():
            return jsonify(inventory.count_by_status())

        return app


# ─────────────────────────────────────────────
# Демо деректер / Demo data helper
# ─────────────────────────────────────────────

def generate_demo_inventory(seed: int = 42) -> LabInventory:
    """Жобаны тексеру үшін демо инвентарь / Generate demo inventory for testing."""
    random.seed(seed)
    inv = LabInventory(name="NIS Computer Lab")

    rooms = ["101", "102", "103", "104"]
    statuses = [
        DeviceStatus.WORKING,  DeviceStatus.WORKING,  DeviceStatus.WORKING,
        DeviceStatus.BROKEN,   DeviceStatus.REPAIR,   DeviceStatus.RETIRED,
    ]

    pc_num = 1
    for room in rooms:
        for i in range(1, 9):   # 8 PCs per room
            pc_id  = f"PC-{room}-{i:02d}"
            status = random.choice(statuses)
            inv.add_device(Device(pc_id=pc_id, status=status, room=room))
            pc_num += 1

    return inv
