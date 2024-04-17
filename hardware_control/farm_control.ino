#include <DHT11.h>

const int temp_sensor_pin = 2;  //온습도 센서 핀 2번

int temperature = 0;
int humidity = 0;

DHT11 dht11(temp_sensor_pin);

void setup() {
    Serial.begin(9600);
    
    // dht11.setDelay(500); // Set this to the desired delay. Default is 500ms.
}

void loop() {
  int temp_result = dht11.readTemperatureHumidity(temperature, humidity);   //temperature, humidity에 온습도 측정값 저장, temp_result의 인식 성공 결과 저장

  serialPrint(temp_result);   //시리얼 출력
}

void serialPrint(int temp_result)
{
  if (temp_result == 0)
  {
      Serial.print(temperature);
      Serial.print(",");
      Serial.println(humidity);
  }
  else
  {
    Serial.println(DHT11::getErrorString(temp_result));
  }
}