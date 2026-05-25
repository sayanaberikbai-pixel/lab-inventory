"""
main.py – Барлық 14 тапсырманы орындайтын демо скрипт
Runs all 14 tasks as a complete demo.
"""

from pathlib import Path
from lab_inventory import (
    Device, DeviceStatus, LabInventory, generate_demo_inventory
)


def separator(title: str) -> None:
    print(f"\n{'─' * 55}")
    print(f"  {title}")
    print('─' * 55)


def main() -> None:

    # ── Tasks 1-3: Device creation & validation ───────────────────────
    separator("Tasks 1-3 | Жабдық жасау және тексеру")

    pc1 = Device(pc_id="PC-101-01", status=DeviceStatus.WORKING, room="101")
    pc2 = Device(pc_id="PC-101-02", status="broken",             room="101")
    pc3 = Device(pc_id="PC-102-01", status=DeviceStatus.REPAIR,  room="102")
    print(f"pc1 → {pc1}")
    print(f"pc2 → {pc2}")
    print(f"pc3 → {pc3}")
    print(f"pc1 жұмыс істей ме? {pc1.is_operational()}")
    print(f"pc2 жұмыс істей ме? {pc2.is_operational()}")

    # Validation errors
    for bad, kwargs in [
        ("бос pc_id",  dict(pc_id="",    status="working", room="101")),
        ("жарамсыз status", dict(pc_id="X", status="flying",  room="101")),
        ("бос room",   dict(pc_id="X",    status="working", room=""   )),
    ]:
        try:
            Device(**kwargs)
        except ValueError as e:
            print(f"  ✗ Validation [{bad}]: {e}")

    # ── Tasks 4-6: LabInventory CRUD & summary ────────────────────────
    separator("Tasks 4-6 | LabInventory CRUD және қорытынды")

    inv = generate_demo_inventory()
    print(inv.summary())

    # Update
    inv.update_status("PC-101-01", DeviceStatus.BROKEN)
    print(f"\nPC-101-01 жаңа күй / new status: {inv.get_device('PC-101-01').status}")

    # Filter
    broken = inv.filter_by_status(DeviceStatus.BROKEN)
    print(f"Ақаулы жабдықтар / Broken devices: {len(broken)}")

    room_101 = inv.filter_by_room("101")
    print(f"101-аудитория / Room 101 devices: {len(room_101)}")

    # ── Task 7: Broken devices generator ─────────────────────────────
    separator("Task 7 | Ақаулы жабдықтар генераторы")

    print("Ақаулы / жөндеудегі жабдықтар:")
    for dev in inv.broken_devices():
        print(f"  {dev.pc_id:15} | {dev.status.value:10} | Аудитория: {dev.room}")

    # ── Task 8: JSON serialization ────────────────────────────────────
    separator("Task 8 | JSON сериализация")

    json_path = inv.to_json("data/inventory.json")
    print(f"Сақталды / Saved → {json_path}")

    inv2 = LabInventory.from_json(json_path)
    print(f"Жүктелді / Loaded ← {json_path}  ({len(inv2.all_devices())} devices)")

    # ── Tasks 9-10: Pandas groupby ────────────────────────────────────
    separator("Tasks 9-10 | Pandas groupby(room, status)")

    grouped = inv.groupby_room_status()
    print(grouped.to_string(index=False))

    # ── Task 11: Pivot table ──────────────────────────────────────────
    separator("Task 11 | Pivot кестесі")

    pivot = inv.pivot_table()
    print(pivot)

    # ── Task 12: Room summary table ───────────────────────────────────
    separator("Task 12 | Аудитория бойынша қорытынды кесте")

    summary_tbl = inv.room_summary_table()
    print(summary_tbl)

    # ── Task 13: Bar chart ────────────────────────────────────────────
    separator("Task 13 | Bar-диаграмма")

    chart_path = inv.plot_status_bar("reports/status_bar.png")
    print(f"Диаграмма сақталды / Chart saved → {chart_path}")

    # ── Task 14: Flask API (show routes) ─────────────────────────────
    separator("Task 14 | Flask REST API маршруттары")

    app = inv.create_flask_app()
    print("Flask API маршруттары / routes:")
    for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
        if not rule.rule.startswith("/static"):
            print(f"  {list(rule.methods - {'HEAD','OPTIONS'})}  {rule.rule}")

    print("\n✅ Барлық тапсырмалар орындалды / All tasks completed!")
    print("   python main.py --api    →  API серверін іске қосу / Start API server")


def run_api() -> None:
    """Flask серверін іске қосу / Launch the Flask development server."""
    inv = generate_demo_inventory()
    app = inv.create_flask_app()
    print("🚀  http://127.0.0.1:5000/api/report")
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    import sys
    if "--api" in sys.argv:
        run_api()
    else:
        main()
