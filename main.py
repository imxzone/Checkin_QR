# main.py
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import re
from scan_qr import scan_qr

GUEST_CSV = "guests.csv"
JSON_OUTPUT_DIR = Path("json_output")
JSON_OUTPUT_DIR.mkdir(exist_ok=True)

def load_guests():
    try:
        df = pd.read_csv(GUEST_CSV)
        print(f"Đã load {len(df)} khách từ {GUEST_CSV}")
        return {
            str(row["guest_id"]): {
                "guest_id": str(row["guest_id"]),
                "full_name": row.get("full_name", ""),
                "email": row.get("email", ""),
                "company": row.get("company", ""),
            }
            for _, row in df.iterrows()
        }
    except FileNotFoundError:
        print(f"Không tìm thấy {GUEST_CSV}. Sẽ chỉ lưu raw QR data.")
        return {}

guest_dict = load_guests()

def slugify(text):
    return re.sub(r"[^0-9a-zA-Z]+", "_", text).strip("_") or "qr_data"

def save_json(qr_data):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if qr_data in guest_dict:
        info = guest_dict[qr_data]
        data = {"timestamp": now, **info}
        filename = f"{qr_data}.json"
        print(f"Lưu JSON cho khách: {qr_data}")
    else:
        data = {"timestamp": now, "raw_data": qr_data}
        filename = f"{slugify(qr_data)}.json"
        print(f"Lưu JSON RAW: {qr_data}")

    json_path = JSON_OUTPUT_DIR / filename
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Đã lưu file: {json_path}\n")

if __name__ == "__main__":
    print("BẮT ĐẦU CHECK-IN BẰNG QR")
    qr_text = scan_qr()

    if qr_text:
        save_json(qr_text)
    else:
        print("Không quét được QR nào.")
