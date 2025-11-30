import qrcode
import pandas as pd
from pathlib import Path

INPUT_CSV = "guests.csv"
OUTPUT_DIR = Path("qrcodes")

OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(INPUT_CSV)

for _, row in df.iterrows():
    guest_id = row["guest_id"]
    # Dữ liệu bạn muốn encode (ở đây chỉ encode guest_id cho đơn giản)
    data = guest_id

    img = qrcode.make(data)
    img.save(OUTPUT_DIR / f"{guest_id}.png")

print("Đã tạo QR cho tất cả khách mời.")
