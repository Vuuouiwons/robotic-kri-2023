#include "MPU9150_9Axis_MotionApps41.h"

#define ENCXEnable 9                    // Pengatur kapan encoder harus membaca
#define ENCXA 19                         // Bagian A dari encoder  (Lihat cara kerja encoder kalau tidak mengerti)
#define ENCXB 18                         // Bagian B dari encoder
#define ENCYEnable 8
#define ENCYA 2
#define ENCYB 3

#define IrPin A0

int irValue = 0; //ir

//mpu

int num, a, b; //a itu koor x//b itu koor y

MPU9150 mpu;

float finalMPUValue;

char currentOp = 'o';
char lastOp = 'o';

char trig = 'x';

bool dmpReady = false;  // set true if DMP init was successful
uint8_t mpuIntStatus;   // holds actual interrupt status byte from MPU
uint8_t devStatus;      // return status after each device operation (0 = success, !0 = error)
uint16_t packetSize;    // expected DMP packet size (default is 42 bytes)
uint16_t fifoCount;     // count of all bytes currently in FIFO
uint8_t fifoBuffer[64]; // FIFO storage buffer

Quaternion q;           // [w, x, y, z]         quaternion container
VectorFloat gravity;    // [x, y, z]            gravity vector
float euler[3];         // [psi, theta, phi]    Euler angle container
float ypr[3];           // [yaw, pitch, roll]   yaw/pitch/roll container and gravity vector

float yaw;                                                      //Pembacaan sudut asli
float lastyaw;                                                  //Pembacaan sudut sebelumnya
float calibration_value = 0;                                    //Nilai untuk mereset posisi robot
float calibrated_value = 0;                                     //Nilai untuk posisi robot

volatile bool mpuInterrupt = false;     // indicates whether MPU interrupt pin has gone high

char output[22] = "#000|-0000|-0000|0|0|0|";

bool sudahKalibrasi = false;

void dmpDataReady() {
  mpuInterrupt = true;
}

void MPU() {
  // if programming failed, don't try to do anything
  if (!dmpReady)
    return;

  mpu.resetFIFO();
  mpuIntStatus = mpu.getIntStatus();
  fifoCount = mpu.getFIFOCount();
  if ((mpuIntStatus & 0x10) || fifoCount == 1024) {
    mpu.resetFIFO();
  }

  else if (mpuIntStatus & 0x02) {
    while (fifoCount < packetSize) fifoCount = mpu.getFIFOCount();

    mpu.getFIFOBytes(fifoBuffer, packetSize);
    fifoCount -= packetSize;

    mpu.dmpGetQuaternion(&q, fifoBuffer);
    mpu.dmpGetGravity(&gravity, &q);
    mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);

    yaw = ypr[0] * 180 / M_PI;

    calibrated_value = yaw - calibration_value + 180;  // Membuat agar posisi default robot 180 derajat

    if (calibrated_value > 359.99)                        // Bila melewati batas satu putaran 360 derajat, dikembalikan ke posisi awal
      calibrated_value = calibrated_value - 360.0;

    else if (calibrated_value < 0.00)                     // Bila berkurang dari 0 derajat balik menjadi 360 kurang
      calibrated_value = calibrated_value + 360.0;

    finalMPUValue = 360 - calibrated_value;
  }
}

//Encoder
volatile int counter = 0;  //This variable will increase or decrease depending on the rotation of encoder
float counterX = 0;
float counterY = 0;

int pulsa_encoder = 100;
float diameter_roda = 6; //cm

float jarakX = 0;
float jarakY = 0;

void setupMPU(){
  #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    Wire.begin();
  TWBR = 24; // 400kHz I2C clock (200kHz if CPU is 8MHz)

  #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
    Fastwire::setup(400, true);
  #endif
  
  while (!Serial);
  mpu.initialize();
  devStatus = mpu.dmpInitialize();

  if (devStatus == 0) {
    mpu.setDMPEnabled(true);
    dmpReady = true;
    packetSize = mpu.dmpGetFIFOPacketSize();
  }

  delay(100);

  int start = millis();

//  Serial.println(start);
  
  do {
    MPU();
    lastyaw = abs(yaw);
    Serial.print(lastyaw);
    for (int i = 0; i < 5; i++)
      MPU();
    Serial.print('\t'); Serial.println(yaw);
    //Serial.print(String(millis())+"\t");Serial.println(String(start));
  } while (abs(abs(yaw) - lastyaw) > 0.01 || millis()<start+1000);

  calibration_value = calibrated_value;

  Serial.println("READY");
}

void setupENCODER(){
  pinMode(ENCXEnable, OUTPUT);
  pinMode(ENCYEnable, OUTPUT);

  attachInterrupt(4, XA, RISING);
  attachInterrupt(5, XB, RISING);

  attachInterrupt(digitalPinToInterrupt(ENCYA), YA, RISING);

  digitalWrite(ENCYEnable, HIGH);
  digitalWrite(ENCXEnable, HIGH);
}

void setup() {
  Serial.begin(500000);

  pinMode(IrPin, INPUT);

  setupMPU();
  setupENCODER();

}

void encodeString(){
  
  char mpuchar[3];
  dtostrf(finalMPUValue,3,0,mpuchar);

  char Xchar[5];
  dtostrf(jarakX * -1 ,5,0,Xchar);

  char Ychar[5];
  dtostrf(jarakY ,5,0,Ychar);
  

  for(int i=1;i<4;i++){
    output[i]=mpuchar[i-1];
  }

  for(int i=5;i<10;i++){
    output[i]=Xchar[i-5];
  }

  for(int i=11;i<16;i++){
    output[i]=Ychar[i-11];
  }

  output[17] = char(irValue+48);
}

void loop(){
  MPU();

  encodeString();

  irValue = digitalRead(IrPin);
  
  if(Serial.available()){
    trig = Serial.read();
    if(trig == 'o'){
      Serial.write(output);
      trig = 'x';
    }
  }

  Serial.write(output);
  Serial.println();

}

void XA() {
  // ai0 is activated if DigitalPin nr 2 is going from LOW to HIGH
  // Check pin 3 to determine the direction
  if (digitalRead(ENCXB) == LOW) {
    counter++;
    counterX += counter * cos(calibrated_value * M_PI / 180); // Jika Encoder menghadap ke belakang(counter++),Jika Encoder menghadap ke depan(counter--)
    counterY += counter * sin(calibrated_value * M_PI / 180);
    jarakX -= cos(calibrated_value * M_PI / 180) * diameter_roda * 22 / 7 / pulsa_encoder / 2;
    jarakY += sin(calibrated_value * M_PI / 180) * diameter_roda * 22 / 7 / pulsa_encoder / 2;
  }

  else {
    counter--;
    counterX -= counter * cos(calibrated_value * M_PI / 180); // Jika Encoder menghadap ke belakang(counter--),Jika Encoder menghadap ke depan(counter++)
    counterY -= counter * sin(calibrated_value * M_PI / 180);
    jarakX += cos(calibrated_value * M_PI / 180) * diameter_roda * 22 / 7 / pulsa_encoder / 2;
    jarakY -= sin(calibrated_value * M_PI / 180) * diameter_roda * 22 / 7 / pulsa_encoder / 2;
  }
}

void XB() {
  // ai0 is activated if DigitalPin nr 3 is going from LOW to HIGH
  // Check with pin 2 to determine the direction
  if (digitalRead(ENCXA) == LOW) {
    counter--;
    counterX -= counter * cos(calibrated_value * M_PI / 180); // Jika Encoder menghadap ke belakang(counter--),Jika Encoder menghadap ke depan(counter++)
    counterY -= counter * sin(calibrated_value * M_PI / 180);
    jarakX += cos(calibrated_value * M_PI / 180) * diameter_roda * 22 / 7 / pulsa_encoder / 2;
    jarakY -= sin(calibrated_value * M_PI / 180) * diameter_roda * 22 / 7 / pulsa_encoder / 2;
  }

  else {
    counter++;
    counterX += counter * cos(calibrated_value * M_PI / 180); // Jika Encoder menghadap ke belakang(counter++),Jika Encoder menghadap ke depan(counter--)
    counterY += counter * sin(calibrated_value * M_PI / 180);
    jarakX -= cos(calibrated_value * M_PI / 180) * diameter_roda * 22 / 7 / pulsa_encoder / 2;
    jarakY += sin(calibrated_value * M_PI / 180) * diameter_roda * 22 / 7 / pulsa_encoder / 2;
  }
}

void YA() {
  // ai0 is activated if DigitalPin nr 2 is going from LOW to HIGH
  // Check pin 3 to determine the direction
  if (digitalRead(ENCYB) == LOW) {

    //counter--;
    //counterX-=counter*sin(calibrated_value*M_PI/180); // Jika Encoder menghadap ke belakang(counter++),Jika Encoder menghadap ke depan(counter--)
    //counterY-=counter*cos(calibrated_value*M_PI/180);
    jarakX -= sin(calibrated_value * M_PI / 180) * diameter_roda * 22 / 7 / pulsa_encoder / 2;
    jarakY -= cos(calibrated_value * M_PI / 180) * diameter_roda * 22 / 7 / pulsa_encoder / 2;
    //Serial.println(jarakY);//Serial.print("\tYA,YB=LOW");
  }

  else {
    //counter++;
    //counterX+=counter*sin(calibrated_value*M_PI/180); // Jika Encoder menghadap ke belakang(counter--),Jika Encoder menghadap ke depan(counter++)
    //counterY+=counter*cos(calibrated_value*M_PI/180);
    jarakX += sin(calibrated_value * M_PI / 180) * diameter_roda * 22 / 7 / pulsa_encoder / 2;
    jarakY += cos(calibrated_value * M_PI / 180) * diameter_roda * 22 / 7 / pulsa_encoder / 2;
    //Serial.println(jarakY);//Serial.print("\tYA,YB=HIGH");
  }
}

void YB() {
  // ai0 is activated if DigitalPin nr 3 is going from LOW to HIGH
  // Check with pin 2 to determine the direction
  if (digitalRead(ENCYA) == LOW) {
    //counter++;
    //counterX+=counter*sin(calibrated_value*M_PI/180); // Jika Encoder menghadap ke belakang(counter--),Jika Encoder menghadap ke depan(counter++)
    //counterY+=counter*cos(calibrated_value*M_PI/180);
    jarakX += sin(calibrated_value * 22 / 7 / 180) * diameter_roda * 22 / 7 / pulsa_encoder / 2;
    jarakY += cos(calibrated_value * 22 / 7 / 180) * diameter_roda * 22 / 7 / pulsa_encoder / 2;
    //Serial.println(jarakY);//Serial.print("\tYB,YA=LOW");
  }

  else {
    //counter--;
    //counterX-=counter*sin(calibrated_value*M_PI/180); // Jika Encoder menghadap ke belakang(counter++),Jika Encoder menghadap ke depan(counter--)
    //counterY-=counter*cos(calibrated_value*M_PI/180);
    jarakX -= sin(calibrated_value * 22 / 7 / 180) * diameter_roda * 22 / 7 / pulsa_encoder / 2;
    jarakY -= cos(calibrated_value * 22 / 7 / 180) * diameter_roda * 22 / 7 / pulsa_encoder / 2;
    //Serial.println(jarakY);//Serial.print("\tYB,YA=HIGH");
  }
}
