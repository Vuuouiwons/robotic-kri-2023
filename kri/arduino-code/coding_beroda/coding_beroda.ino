#define aVIN 4 // 9 // Pengatur kecepatan motor A KIRI DEPANlastShoot
#define aIN1 22 // 24 // Pengatur arah putar motor A
#define aIN2 24 // 22 // Pengatur arah putar motor A

#define bVIN 5 // 10// KANAN DEPAN
#define bIN1 28 // 28
#define bIN2 30 // 26

#define cVIN 6 // 11 // BELAKANG
#define cIN1 34 // 30
#define cIN2 36 // 32

#define drib1VIN 12
#define drib1IN1 37
#define drib1IN2 35

#define drib2VIN 13
#define drib2IN1 41
#define drib2IN2 39

#define shooter 43

int pwmRoda = 40, pwmDrible = 200;
String action = "o";

void setup() {
  Serial.begin(500000);
  
  pinMode(aVIN, OUTPUT);
  pinMode(bVIN, OUTPUT);
  pinMode(cVIN, OUTPUT);

  pinMode(aIN1, OUTPUT);
  pinMode(bIN1, OUTPUT);
  pinMode(cIN1, OUTPUT);

  pinMode(aIN2, OUTPUT);
  pinMode(bIN2, OUTPUT);
  pinMode(cIN2, OUTPUT);
  
  pinMode(drib1VIN,OUTPUT);
  pinMode(drib1IN1,OUTPUT);
  pinMode(drib1IN2,OUTPUT);
  
  pinMode(drib2VIN,OUTPUT);
  pinMode(drib2IN1,OUTPUT);
  pinMode(drib2IN2,OUTPUT);

  pinMode(shooter,OUTPUT);
}

void loop() {

  // Serial.println("maju");
  // maju(1000);
  
  // Serial.println("wiaitting");
  // parking(2000);
  
  

  if(Serial.available()){
      action = Serial.readStringUntil('\n');
      
      if(action == "TEST_SERIAL") {
        digitalWrite(LED_BUILTIN, HIGH);
        delay(5000);
        digitalWrite(LED_BUILTIN, LOW);
      }

      Serial.println(action);
  }

  switch(action) {
    case "w":
      maju();
      break;
    case "a":
      kiri();
      break;
    case "s":
      mundur();
      break;
    case "d":
      kanan();
      break;
    case "q":
      putarkiri();
      break;
    case "e":
      putarkanan();
      break;
    case "y":
      drib_on_backward();
      break;
    case "n":
      drib_off();
      break;
    case "+":
      tendang();
      break;
    case "o":
      parking();
      break;
    case "TEST_A":
      testA();
      Serial.println("Motor A");
      break;
    case "TEST_B":
      testB();
      Serial.println("Motor B");
      break;
    case "TEST_C":
      testC();
      Serial.println("motor C");
      break;
    default:
      parking();
      Serial.println("Unknown Input Robot Stopping....")
      break;
  }
}

void tendang(){
  digitalWrite(shooter,HIGH);
  delay(1000);
  digitalWrite(shooter,LOW);
  action3 = "-";
}

void testA() {
  Serial.println("jalan");
  digitalWrite(aIN1, LOW);
  digitalWrite(aIN2, HIGH);
  analogWrite(aVIN, pwmRoda);

  digitalWrite(bIN1, LOW);
  digitalWrite(bIN2, LOW);
  analogWrite(bVIN, pwmRoda);

  digitalWrite(cIN1, LOW);
  digitalWrite(cIN2, LOW);
  analogWrite(cVIN, pwmRoda);
}

void testB() {

  digitalWrite(aIN1, LOW);
  digitalWrite(aIN2, LOW);
  analogWrite(aVIN, pwmRoda);

  digitalWrite(bIN1, LOW);
  digitalWrite(bIN2, HIGH);
  analogWrite(bVIN, pwmRoda);

  digitalWrite(cIN1, LOW);
  digitalWrite(cIN2, LOW);
  analogWrite(cVIN, pwmRoda);
}

void testC() {

  digitalWrite(aIN1, LOW);
  digitalWrite(aIN2, LOW);
  analogWrite(aVIN, pwmRoda);

  digitalWrite(bIN1, LOW);
  digitalWrite(bIN2, LOW);
  analogWrite(bVIN, pwmRoda);

  digitalWrite(cIN1, HIGH);
  digitalWrite(cIN2, HIGH);
  analogWrite(cVIN, pwmRoda);
}



void putarkiri() {

  digitalWrite(aIN1, LOW);
  digitalWrite(aIN2, HIGH);
  analogWrite(aVIN, pwmRoda * 0.5);

  digitalWrite(bIN1, LOW);
  digitalWrite(bIN2, HIGH);
  analogWrite(bVIN, pwmRoda * 0.5);

  digitalWrite(cIN1, LOW);
  digitalWrite(cIN2, HIGH);
  analogWrite(cVIN, pwmRoda * 0.5);
  
}

void putarkanan(){
  
  digitalWrite(aIN1, HIGH);
  digitalWrite(aIN2, LOW);
  analogWrite(aVIN, pwmRoda * 0.5);

  digitalWrite(bIN1, HIGH);
  digitalWrite(bIN2, LOW);
  analogWrite(bVIN, pwmRoda * 0.5);

  digitalWrite(cIN1, HIGH);
  digitalWrite(cIN2, LOW);
  analogWrite(cVIN, pwmRoda * 0.5);
  
}

void kiri(){

  digitalWrite(aIN1, LOW);
  digitalWrite(aIN2, HIGH);
  analogWrite(aVIN, pwmRoda);

  digitalWrite(bIN1, LOW);
  digitalWrite(bIN2, HIGH);
  analogWrite(bVIN, pwmRoda);

  digitalWrite(cIN1, HIGH);
  digitalWrite(cIN2, LOW);
  analogWrite(cVIN, pwmRoda);
  
}

void kanan(){

  digitalWrite(aIN1, HIGH);
  digitalWrite(aIN2, LOW);
  analogWrite(aVIN, pwmRoda);

  digitalWrite(bIN1, HIGH);
  digitalWrite(bIN2, LOW);
  analogWrite(bVIN, pwmRoda);

  digitalWrite(cIN1, LOW);
  digitalWrite(cIN2, HIGH);
  analogWrite(cVIN, pwmRoda);
  
}

void brake(){
  digitalWrite(aIN1, HIGH);
  digitalWrite(aIN2, HIGH);
  analogWrite(aVIN, 15);

  digitalWrite(bIN1, HIGH);
  digitalWrite(bIN2, HIGH);
  analogWrite(bVIN, 15);

  digitalWrite(cIN1, HIGH);
  digitalWrite(cIN2, HIGH);
  analogWrite(cVIN, 15);
  
}

void parking(){
  digitalWrite(aIN1, LOW);
  digitalWrite(aIN2, LOW);
  analogWrite(aVIN, 0);

  digitalWrite(bIN1, LOW);
  digitalWrite(bIN2, LOW);
  analogWrite(bVIN, 0);

  digitalWrite(cIN1, LOW);
  digitalWrite(cIN2, LOW);
  analogWrite(cVIN, 0);
  
}

void mundur(){
  
  digitalWrite(aIN1, LOW);
  digitalWrite(aIN2, HIGH);
  analogWrite(aVIN, pwmRoda);

  digitalWrite(bIN1, HIGH);
  digitalWrite(bIN2, LOW);
  analogWrite(bVIN, pwmRoda);

  digitalWrite(cIN1, HIGH);
  digitalWrite(cIN2, HIGH);
  analogWrite(cVIN, pwmRoda);
  
}

void maju(){
  digitalWrite(aIN1, HIGH);
  digitalWrite(aIN2, LOW);
  analogWrite(aVIN, pwmRoda * 1.3);

  digitalWrite(bIN1, LOW);
  digitalWrite(bIN2, HIGH);
  analogWrite(bVIN, pwmRoda * 1.3);

  digitalWrite(cIN1, HIGH);
  digitalWrite(cIN2, HIGH);
  analogWrite(cVIN, pwmRoda);
  
}

void drib_on_backward(){
  digitalWrite(drib1IN1, HIGH);
  digitalWrite(drib1IN2, LOW);
  analogWrite(drib1VIN, pwmDrible);

  digitalWrite(drib2IN1, HIGH);
  digitalWrite(drib2IN2, LOW);
  analogWrite(drib2VIN, pwmDrible);
}

void drib_on_right(){
  digitalWrite(drib1IN1, LOW);
  digitalWrite(drib1IN2, HIGH);
  analogWrite(drib1VIN, pwmDrible);

  digitalWrite(drib2IN1, HIGH);
  digitalWrite(drib2IN2, LOW);
  analogWrite(drib2VIN, pwmDrible * 1/8);
}

void drib_on_left(){
  digitalWrite(drib1IN1, LOW);
  digitalWrite(drib1IN2, HIGH);
  analogWrite(drib1VIN, pwmDrible * 1/8);

  digitalWrite(drib2IN1, HIGH);
  digitalWrite(drib2IN2, LOW);
  analogWrite(drib2VIN, pwmDrible);
}

void drib_off(){
  digitalWrite(drib1IN1, LOW);
  digitalWrite(drib1IN2, LOW);
  digitalWrite(drib1VIN, LOW);

  digitalWrite(drib2IN1, LOW);
  digitalWrite(drib2IN2, LOW);
  digitalWrite(drib2VIN, LOW);
}