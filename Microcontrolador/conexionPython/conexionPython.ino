
String payload;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(100);

}

void loop() {
  // put your main code here, to run repeatedly:
  delay(100);
  if (Serial.available()){
    payload = Serial.readString();
    Serial.println(payload);
    }

}
