import cv2
from pyzbar.pyzbar import decode
import time

def scan_qr(on_scan=None, delay_seconds=4):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Không mở được webcam (index 0).")
        return

    print("Webcam đã bật. Đưa mã QR vào trước camera.")
    print("Nhấn phím 'q' để thoát.")

    last_message = ""         
    message_expire_time = 0.0 
    next_allowed_scan_time = 0.0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Không đọc được hình từ camera.")
            break

        now = time.time()
        decoded_objects = decode(frame)
        qr_text_display = "Không phát hiện QR"

        if decoded_objects and now >= next_allowed_scan_time:
            obj = decoded_objects[0]
            data = obj.data.decode("utf-8").strip()
            qr_text_display = f"QR: {data}"

            if on_scan is not None:
                try:
                    on_scan(data)
                    last_message = "Check-in thành công"
                except Exception as e:
                    last_message = f"Lỗi khi xử lý: {e}"
            else:
                last_message = "Đã quét mã QR"

            next_allowed_scan_time = now + delay_seconds
            message_expire_time = now + delay_seconds

            pts = obj.polygon
            pts = [(p.x, p.y) for p in pts]
            for i in range(len(pts)):
                cv2.line(frame, pts[i], pts[(i + 1) % len(pts)], (0, 255, 0), 2)

        elif decoded_objects:

            obj = decoded_objects[0]
            data = obj.data.decode("utf-8").strip()
            qr_text_display = f"Đang chờ, vui lòng đợi..."
            pts = obj.polygon
            pts = [(p.x, p.y) for p in pts]
            for i in range(len(pts)):
                cv2.line(frame, pts[i], pts[(i + 1) % len(pts)], (0, 255, 255), 2)

        cv2.putText(
            frame,
            qr_text_display,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2,
        )

        if now < message_expire_time and last_message:
            cv2.putText(
                frame,
                last_message,
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
            )

        cv2.imshow("QR Check-in", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Thoát.")
            break

    cap.release()
    cv2.destroyAllWindows()
