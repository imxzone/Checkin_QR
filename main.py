from pathlib import Path

from src_code.scan_qr import scan_qr
from src_code.load_guests import load_guests
from src_code.save_json import save_json
from src_code.update_checkin import update_checkin

GUEST_CSV = Path("guests.csv")
JSON_OUTPUT_DIR = Path("json_output")

df_guests = None
guest_dict = {}


if __name__ == "__main__":
    print("Bắt đầu check-in bằng QR")
    df_guests, guest_dict = load_guests(GUEST_CSV)

    def handle_qr(qr_text: str):
        global df_guests

        if qr_text in guest_dict:
            df_guests, count = update_checkin(df_guests, qr_text, GUEST_CSV)
            save_json(qr_text, guest_dict, JSON_OUTPUT_DIR, checkin_count=count)
        else:
            save_json(qr_text, guest_dict, JSON_OUTPUT_DIR)
    scan_qr(on_scan=handle_qr, delay_seconds=4)
