#include <DHT11.h>

const char FARM_ID = '1';
const int TEMPERATURE_PIN = A2; 
const int WATER_PIN = A1;
const int TEMPERATURE_ERROR = 5;
const int HUMIDITY_ERROR = 5;
const int WATER_ERROR = 5;
const int MAX_LED = 10;

bool farm_on;

int temperature = 0;
int humidity = 0;
int water = 0;
int led = 0;
int target_temperature = 0;
int target_humidity = 0;
int target_water = 0;
int target_LED = 0;
bool led_on;
int temperature_flag = 0;
int humidity_flag = 0;
int water_flag = 0;


DHT11 dht11(TEMPERATURE_PIN);

int sendCurrentStatus()
{
  Serial.print('S');
  Serial.print(FARM_ID);
  if(farm_on == true)
  {
    Serial.print('Y');
  }
  else
  {
    Serial.print('N');
  }

  char temp_str[30];
  sprintf(temp_str, "%02d", temperature);
  Serial.print(temp_str);

  if(temperature_flag == 1)
  {
    Serial.print('H');
  }
  else if(temperature_flag == 0)
  {
    Serial.print('F');
  }
  else
  {
    Serial.print('C');
  }

  sprintf(temp_str, "%02d", humidity);
  Serial.print(temp_str);

  if(humidity_flag == 1)
  {
    Serial.print('Y');
  }
  else
  {
    Serial.print('N');
  }

  sprintf(temp_str, "%02d", water);
  Serial.print(temp_str);

  if(water_flag == 1)
  {
    Serial.print('Y');
  }
  else
  {
    Serial.print('N');
  }
  Serial.println(target_LED);
}

int Control(int current, int target, int error, int *flag)
{
  if(current < target - error)
  {
    *flag = 1;
  }
  else if(current > target + error)
  {
    *flag = -1;
  }

  if((*flag == 1 && (current >= target)) || (*flag == -1 && (current <= target)))
  {
    *flag = 0;
  }
  return *flag;
}

void setup() {
    Serial.begin(9600);
    farm_on = true;
    led_on = true;
    
}

void loop() {
  String recv_data = "";

  if(Serial.available() > 0)
  {
    recv_data = Serial.readStringUntil('\n');
  }
  if (recv_data.length() > 0)
  {
    Serial.print('R');
    Serial.print(FARM_ID);

    char set = recv_data[0];

    if (set == 'Y' && recv_data.length() == 8)
    {
      farm_on = true;
      target_temperature = recv_data.substring(1,3).toInt();
      target_humidity = recv_data.substring(3,5).toInt();
      target_water = recv_data.substring(5,7).toInt();

      if (recv_data[7] == 'N')
      {
        led_on = false;
      }
      else
      {
        led_on = true;
        target_LED = recv_data[7]-'0';
      }
      Serial.println('Y');
    }
    else if (set == 'N')
    {
      farm_on = false;
      Serial.println('Y');
    }
    else
    {
      Serial.println('N');
    }
  }

  
  dht11.readTemperatureHumidity(temperature, humidity);
  water = map(analogRead(WATER_PIN), 1023, 0, 0, 100);
  led = map(target_LED, 0, MAX_LED, 0, 255);
  int temperature_control = Control(temperature, target_temperature, TEMPERATURE_ERROR, &temperature_flag);
  int humidity_control = Control(humidity, target_humidity, HUMIDITY_ERROR, &humidity_flag);
  int water_control = Control(water, target_water, WATER_ERROR, &water_flag);

  sendCurrentStatus();

  delay(1000);

  




/*
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
  */
}

