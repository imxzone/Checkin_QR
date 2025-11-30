import pandas as pd

def load_guests(guest_csv_path):
    """
    Load danh sách khách từ file CSV và trả về guest_dict.
    """
    try:
        df = pd.read_csv(guest_csv_path)
        print(f"Đã load {len(df)} khách từ {guest_csv_path}")
        if "checkin_time" not in df.columns:
            df["checkin_time"] = ""
        if "checkin_count" not in df.columns:
            df["checkin_count"] = 0

        guest_dict = {
            str(row["guest_id"]): {
                "guest_id": str(row["guest_id"]),
                "full_name": row.get("full_name", ""),
                "email": row.get("email", ""),
                "company": row.get("company", "")
            }
            for _, row in df.iterrows()
        }

        return df, guest_dict

    except FileNotFoundError:
        print(f"Không tìm thấy file {guest_csv_path}. Chỉ có thể lưu raw QR.")
        return {}