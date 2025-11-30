from datetime import datetime

def update_checkin(df_guests, guest_id, guest_csv_path):
    if df_guests is None or df_guests.empty:
        print("Không có dữ liệu khách để cập nhật.")
        return df_guests, None

    mask = df_guests["guest_id"].astype(str) == str(guest_id)
    if not mask.any():
        print(f"guest_id {guest_id} không tồn tại trong guests.csv.")
        return df_guests, None

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Lấy count cũ, nếu NaN thì coi như 0
    old_count = (
        df_guests.loc[mask, "checkin_count"]
        .fillna(0)
        .astype(int)
        .iloc[0]
    )
    new_count = old_count + 1

    df_guests.loc[mask, "checkin_time"] = now
    df_guests.loc[mask, "checkin_count"] = new_count

    # Ghi đè lại file CSV
    df_guests.to_csv(guest_csv_path, index=False)
    print(
        f"Cập nhật guests.csv: guest_id={guest_id}, "
        f"checkin_time={now}, checkin_count={new_count}"
    )

    return df_guests, new_count
