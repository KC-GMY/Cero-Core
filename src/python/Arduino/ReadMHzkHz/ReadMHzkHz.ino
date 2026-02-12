#include <SoftwareSerial.h>
#include <SPI.h>
#include <MFRC522.h>

// ===================== RDM6300 (kHz) =====================
static const uint8_t STX = 2;
static const uint8_t ETX = 3;

static const uint8_t BUFFER_SIZE = 14;
static const uint8_t DATA_SIZE   = 10;

struct RFIDData {
  char tag_hex[9];        // 8 chars + '\0'
  uint32_t tag_dec;
  char checksum_hex[3];   // 2 chars + '\0'
  bool checksum_valid;
};

class RDM6300 {
public:
  RDM6300(uint8_t rx, uint8_t tx) : ss(rx, tx) {}

  void begin() {
    ss.begin(9600);
    ss.listen();
    reset();
  }

  bool read(RFIDData &out) {
    while (ss.available()) {
      int v = ss.read();
      if (v < 0) continue;

      uint8_t b = (uint8_t)v;

      if (!in_frame) {
        if (b == STX) {
          in_frame = true;
          index = 0;
          buffer[index++] = b;
        }
        continue;
      }

      if (index >= BUFFER_SIZE) {
        reset();
        continue;
      }

      buffer[index++] = b;

      if (b == ETX) {
        if (index == BUFFER_SIZE) {
          decode(out);
          reset();
          return true;
        }
        reset();
      }
    }
    return false;
  }

private:
  SoftwareSerial ss;
  uint8_t buffer[BUFFER_SIZE];
  uint8_t index = 0;
  bool in_frame = false;

  void reset() {
    index = 0;
    in_frame = false;
  }

  static long hex_to_val(const uint8_t *s, uint8_t len) {
    char tmp[9];
    for (uint8_t i = 0; i < len; i++) tmp[i] = (char)s[i];
    tmp[len] = '\0';
    return strtol(tmp, nullptr, 16);
  }

  void decode(RFIDData &out) {
    for (uint8_t i = 0; i < 8; i++) out.tag_hex[i] = (char)buffer[3 + i];
    out.tag_hex[8] = '\0';

    out.tag_dec = (uint32_t)hex_to_val((const uint8_t*)out.tag_hex, 8);

    out.checksum_hex[0] = (char)buffer[11];
    out.checksum_hex[1] = (char)buffer[12];
    out.checksum_hex[2] = '\0';

    long calc = 0;
    for (uint8_t i = 0; i < DATA_SIZE; i += 2) {
      calc ^= hex_to_val(buffer + 1 + i, 2);
    }
    long rx = hex_to_val(buffer + 11, 2);
    out.checksum_valid = (calc == rx);
  }
};

RDM6300 rfid(6, 8);

// ===================== MFRC522 (MHz) =====================
#define RST_PIN  9
#define SS_PIN   10
MFRC522 mfrc522(SS_PIN, RST_PIN);

enum Mode : uint8_t {
  MODE_MHz = 0,
  MODE_kHz = 1
};

Mode mode = MODE_MHz;

void setModeByte(uint8_t b) {
  mode = (b == 0x00) ? MODE_MHz : MODE_kHz;
  Serial.println(mode == MODE_MHz ? "MODE:MHz" : "MODE:kHz");
}

void setup() {
  Serial.begin(9600);

  SPI.begin();
  mfrc522.PCD_Init();
  rfid.begin();

  // --- SIMPLE: give PC time to open port and send mode ---
  unsigned long t0 = millis();
  while (millis() - t0 < 1200) {          // 1.2s window
    if (Serial.available()) {
      uint8_t b = (uint8_t)Serial.read();
      if (b == 0x00 || b == 0x01) {
        setModeByte(b);
        while (Serial.available()) Serial.read();
        break;
      }
    }
  }
}

// ===================== Serial mode switch (raw bytes) =====================
void handleModeSwitch() {
  if (!Serial.available()) return;
  uint8_t b = (uint8_t)Serial.read();
  if (b == 0x00 || b == 0x01) {
    setModeByte(b);
    while (Serial.available()) Serial.read();
  }
}

// ===================== Loops per mode =====================
void loopkHz() {
  RFIDData data;
  if (rfid.read(data)) {
    Serial.println(data.tag_hex);
    Serial.println(data.tag_dec);
    Serial.println(data.checksum_hex);
    Serial.println(data.checksum_valid ? 1 : 0);
  }
}

void loopMHz() {
  if (!mfrc522.PICC_IsNewCardPresent()) return;
  if (!mfrc522.PICC_ReadCardSerial()) return;

  for (byte i = 0; i < mfrc522.uid.size; i++) {
    if (i != 0) Serial.print(" ");
    Serial.print(mfrc522.uid.uidByte[i], HEX);
  }
  Serial.println();


  MFRC522::PICC_Type piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);
  Serial.println(mfrc522.PICC_GetTypeName(piccType));

  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();
  delay(50);
}

// ===================== Main loop =====================
void loop() {
  handleModeSwitch();

  if (mode == MODE_MHz) {
    loopMHz();
  } else {
    loopkHz();
  }
}
