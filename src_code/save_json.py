import json
from datetime import datetime
from pathlib import Path
import re

def slugify(text):
    return re.sub(r"[^0-9a-zA-Z]+", "_", text).strip("_") or "qr_data"

def save_json(qr_data, guest_dict, json_output_dir,checkin_count=None):
    json_output_dir = Path(json_output_dir)
    json_output_dir.mkdir(exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if qr_data in guest_dict:
        info = guest_dict[qr_data]
        data = {"timestamp": now, **info}
        if checkin_count is not None:
            data["checkin_count"] = int(checkin_count)
        filename = f"{qr_data}.json"
        print(f"Lưu JSON cho khách: {qr_data}")
    else:
        data = {"timestamp": now, "raw_data": qr_data}
        filename = f"{slugify(qr_data)}.json"
        print(f"Lưu JSON raw: {qr_data}")

    json_path = json_output_dir / filename

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Đã lưu file JSON: {json_path}\n")