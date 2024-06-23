void setup() {
  // Inisialisasi komunikasi serial dengan baud rate 9600
  Serial.begin(9600);
}

void loop() {
  // Periksa apakah ada data yang tersedia di serial buffer
  if (Serial.available() > 0) {
    // Membaca data dari serial buffer
    char receivedCode = Serial.read();

    // Menentukan posisi berdasarkan kode yang diterima
    switch (receivedCode) {
      case '1':
        Serial.println("1 = left");
        break;
      case '2':
        Serial.println("2 = center");
        break;
      case '3':
        Serial.println("3 = right");
        break;
      default:
        Serial.println("Kode tidak dikenal");
        break;
    }
  }
}
