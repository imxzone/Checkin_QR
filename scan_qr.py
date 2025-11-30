import cv2
from pyzbar.pyzbar import decode

def scan_qr():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Không mở được webcam.")
        return None

    print("Webcam đang bật. Đưa QR vào trước camera...")
    print("Nhấn 'q' để thoát.\n")

    last_data = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Không đọc được frame từ webcam.")
            break

        decoded_objects = decode(frame)
        qr_text_display = "No QR detected"

        for obj in decoded_objects:
            data = obj.data.decode("utf-8").strip()
            qr_text_display = f"QR: {data}"

            if data != last_data:  # tránh đọc lặp
                last_data = data
                print(f"Đã quét được QR: {data}")
                cap.release()
                cv2.destroyAllWindows()
                return data

            # Vẽ khung quanh QR
            pts = obj.polygon
            pts = [(p.x, p.y) for p in pts]
            for i in range(len(pts)):
                cv2.line(frame, pts[i], pts[(i + 1) % len(pts)], (0, 255, 0), 2)

        cv2.putText(frame, qr_text_display, (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        cv2.imshow("QR Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Thoát không quét nữa.")
            break

    cap.release()
    cv2.destroyAllWindows()
    return None
