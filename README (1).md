# 🖥️ Computer Lab Inventory System
### Компьютерлік сыныптың инвентарлық жүйесі

Python OOP жобасы — 14 тапсырма | Full Python OOP project — 14 tasks

---

## 📋 Тапсырмалар / Tasks

| # | Тақырып / Topic | Файл |
|---|---|---|
| 1-3 | `Device` класы, `DeviceStatus` enum, валидация | `lab_inventory.py` |
| 4-6 | `LabInventory` CRUD, сүзу, қорытынды | `lab_inventory.py` |
| 7 | `broken_devices()` генераторы | `lab_inventory.py` |
| 8 | JSON сериализация / десериализация | `lab_inventory.py` |
| 9-12 | Pandas: `groupby`, pivot, қорытынды кесте | `lab_inventory.py` |
| 13 | Matplotlib bar-диаграмма | `lab_inventory.py` |
| 14 | Flask REST API (`/api/report`) | `lab_inventory.py` |

---

## 🏗️ Жоба құрылымы / Project structure

```
lab_inventory/
├── lab_inventory.py      # Негізгі OOP класы / Main OOP class
├── main.py               # Барлық тапсырмалар демосы / All-tasks demo
├── requirements.txt
├── data/
│   └── inventory.json    # (auto-generated)
├── reports/
│   └── status_bar.png    # (auto-generated)
└── tests/
    └── test_lab_inventory.py
```

---

## ⚡ Жылдам бастау / Quick start

```bash
# 1. Клондау / Clone
git clone https://github.com/<your-username>/lab-inventory.git
cd lab-inventory

# 2. Орнату / Install
pip install -r requirements.txt

# 3. Демо іске қосу / Run demo (all 14 tasks)
python main.py

# 4. API серверін іске қосу / Start API server
python main.py --api

# 5. Тесттер / Run tests
pytest tests/ -v
```

---

## 🌐 API маршруттары / Endpoints

| Method | URL | Сипаттама |
|--------|-----|-----------|
| GET | `/api/report` | Барлық аудитория есебі |
| GET | `/api/report/<room>` | Бір аудитория есебі |
| GET | `/api/devices` | Барлық жабдықтар |
| GET | `/api/status_counts` | Күй бойынша санақ |

---

## 🔑 Негізгі класс / Core class

```python
from lab_inventory import Device, DeviceStatus, LabInventory

inv = LabInventory(name="101-аудитория")
inv.add_device(Device("PC-01", DeviceStatus.WORKING, "101"))
inv.add_device(Device("PC-02", DeviceStatus.BROKEN,  "101"))

print(inv.summary())
inv.to_json("data/inv.json")
inv.plot_status_bar("reports/bar.png")

for broken in inv.broken_devices():   # generator
    print(broken)
```

---

## 🧪 Тест нәтижелері / Test results

```
tests/test_lab_inventory.py ............................  28 passed
```
