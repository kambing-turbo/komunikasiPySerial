import cv2
import serial
import time

# Fungsi untuk mencoba membuka port serial
def open_serial_port(port, baud_rate, retries=5, delay=2):
    for attempt in range(retries):
        try:
            ser = serial.Serial(port, baud_rate)
            return ser
        except serial.SerialException:
            print(f"Attempt {attempt + 1} of {retries} failed. Retrying in {delay} seconds...")
            time.sleep(delay)
    raise serial.SerialException(f"Could not open port {port} after {retries} attempts.")

# Inisialisasi komunikasi serial dengan Arduino
ser = open_serial_port('/dev/ttyACM0', 9600)

time.sleep(2)  # Tunggu 2 detik agar koneksi serial stabil

faceRef = cv2.CascadeClassifier("faceRef.xml")
camera = cv2.VideoCapture(0)

def faceDetect(frame): # fungsi untuk mengenali wajah manusia
    optimizedFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # mengoptimalkan frame 
    faces = faceRef.detectMultiScale(optimizedFrame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

def drawBox(frame):
    faces = faceDetect(frame)
    height, width, _ = frame.shape
    position_code = 0  # Inisialisasi dengan kode posisi 0 (tidak ada wajah terdeteksi)
    for x, y, w, h in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        center_x = x + w // 2
        if center_x < width // 3:
            position = "Left"
            position_code = 1
        elif center_x > 2 * width // 3:
            position = "Right"
            position_code = 3
        else:
            position = "Center"
            position_code = 2
        print(f"Coordinates: ({x}, {y}), Position: {position}")
        cv2.putText(frame, position, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    return position_code

def closeWindow():
    camera.release()
    cv2.destroyAllWindows()
    ser.close()
    exit()

def main():
    last_sent_time = time.time()
    while True: # ketika true maka program akan berjalan hingga user menekan "q"
        _, frame = camera.read() # memberikan akses kamera & program ini bakal dapet akses perframe
        position_code = drawBox(frame) # frame yang telah didapat dikirim ke void drawBox

        # Kirim posisi ke Arduino setiap detik
        current_time = time.time()
        if current_time - last_sent_time >= 1:
            ser.write(str(position_code).encode())
            last_sent_time = current_time

        cv2.imshow("face", frame)

        if cv2.waitKey(1) & 0xFF == 27: # tekan 'Esc' untuk keluar
            closeWindow()

if __name__ == "__main__":
    main()