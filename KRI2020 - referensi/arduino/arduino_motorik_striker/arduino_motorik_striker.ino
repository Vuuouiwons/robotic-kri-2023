  
#define aVIN 9                         // Pengatur kecepatan motor A KIRI DEPAN
#define aIN1 25                         // Pengatur arah putar motor A
#define aIN2 23                         // Pengatur arah putar motor A

#define bVIN 10     //KANAN DEPAN
#define bIN1 29
#define bIN2 27

#define cVIN 11     //BELAKANG
#define cIN1 31U
#define cIN2 33

#define drib1VIN 12
#define drib1IN1 37
#define drib1IN2 35

#define drib2VIN 13
#define drib2IN1 41
#define drib2IN2 39

#define shooter 43

int pwmRoda = 40, pwmDrible = 200;

char action1 = 'o', action2 = 'n', action3 = '-', actionTest = 'o';

int lastShoot, now;

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

  pinMode(shooter,OUTPUT);
  
  pinMode(drib1VIN,OUTPUT);
  pinMode(drib1IN1,OUTPUT);
  pinMode(drib1IN2,OUTPUT);
  
  pinMode(drib2VIN,OUTPUT);
  pinMode(drib2IN1,OUTPUT);
  pinMode(drib2IN2,OUTPUT);
}

void loop() {
  if(Serial.available()){
      char input = Serial.read();
      if(input == 'a' || input == 'd' || input == 'o' || input == 'q' || input == 'e' || input == 'w' || input == 's')
        action1 = input;
      else if(input == 'y' || input == 'n'){
        action2 = input;
      }
      else if(input == '+'){
        action3 = input;
      }else{
        actionTest = input;
      }

      Serial.println(input);
  }

  if(action1 == 'a'){
//    testB();
    kiri();
  }
  else if(action1 == 'd'){
    kanan();
  }
  else if(action1 == 'o'){
    parking();
  }
  else if(action1 == 'q'){
    putarkiri();
  }
  else if(action1 == 'e'){
    putarkanan();
  }
  else if(action1 == 'w'){
    maju();
  }
  else if(action1 == 's'){
    mundur();
  }

  if(action2 == 'n'){
    drib_off();
  }
  else if(action2 == 'y'){
    drib_on_backward();
  }

  if(action3 == '+'){
    tendang();
  }

  if(actionTest == 'm'){
    testA();
    Serial.println("Motor A");
  }
  else if(actionTest == 'n'){
    testB();
    Serial.println("Motor B");
  }
  else if(actionTest == 'b'){
    testC();
    Serial.println("motor C");
  }
}

void tendang(){
  digitalWrite(shooter,HIGH);
  delay(1000);
  digitalWrite(shooter,LOW);
  action3 = '-';
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

void putarkanan() {
  
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

void kiri() {

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

void kanan() {

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

void brake() {
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

void parking() {
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
