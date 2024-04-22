#include <DHT11.h>

const char FARM_ID = '1';
const int TEMPERATURE_PIN = A2; 
const int WATER_PIN = A1;
const int FELTIER_PINA = 5;
const int FELTIER_PINB = 6;
const int HUMIDIFIER_PIN =4;
const int PUMP_PIN = 7;
const int FAN_PINA = 2;
const int FAN_PINB = 3; 
const int TEMPERATURE_ERROR = 5;
const int HUMIDITY_ERROR = 5;
const int WATER_ERROR = 5;
const int MAX_LED = 10;
const int SEND_STATUS_DELAY = 1000;

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

unsigned long before_time = 0;

DHT11 dht11(TEMPERATURE_PIN);

int sendCurrentStatus()
{
  unsigned long now = millis();
  if(now - before_time >= SEND_STATUS_DELAY)
  {
    before_time = now;
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
    if (led_on == true)
    {
      Serial.println(target_LED);
    }
    else
    {
      Serial.println('N');
    }
  }
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
    pinMode(FELTIER_PINA, OUTPUT);
    pinMode(FELTIER_PINB, OUTPUT);;
    pinMode(HUMIDIFIER_PIN, OUTPUT);
    pinMode(PUMP_PIN, OUTPUT);
    pinMode(FAN_PINA, OUTPUT);
    pinMode(FAN_PINB, OUTPUT);
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
      target_temperature = max(0, min(99, recv_data.substring(1,3).toInt()));
      target_humidity = max(0, min(99, recv_data.substring(3,5).toInt()));
      target_water = max(0, min(99,recv_data.substring(5,7).toInt()));

      if (recv_data[7] == 'N')
      {
        led_on = false;
      }
      else
      {
        led_on = true;
        target_LED = recv_data[7]-'0';
      }
      Serial.println('S');
    }
    else if (set == 'N' && recv_data.length() == 1)
    {
      farm_on = false;
      led_on = false;
      Serial.println('S');
    }
    else
    {
      Serial.println('F');
    }
  }

  
  dht11.readTemperatureHumidity(temperature, humidity);
  water = map(analogRead(WATER_PIN), 1023, 0, 0, 100);
  led = map(target_LED, 0, MAX_LED, 0, 255);
  int temperature_control = Control(temperature, target_temperature, TEMPERATURE_ERROR, &temperature_flag);
  int humidity_control = Control(humidity, target_humidity, HUMIDITY_ERROR, &humidity_flag);
  int water_control = Control(water, target_water, WATER_ERROR, &water_flag);

  if(farm_on == true)
  {
    digitalWrite(FAN_PINA, HIGH);
    digitalWrite(FAN_PINB, LOW);

    if(temperature_control == 1)
    {
      digitalWrite(FELTIER_PINA, HIGH);
      digitalWrite(FELTIER_PINB, LOW);
    }
    else if(temperature_control == -1)
    {
      digitalWrite(FELTIER_PINA, LOW);
      digitalWrite(FELTIER_PINB, HIGH);
    }
    else
    {
      digitalWrite(FELTIER_PINA, LOW);
      digitalWrite(FELTIER_PINB, LOW);
    }

    if(humidity_control == 1)
    {
      digitalWrite(HUMIDIFIER_PIN, HIGH);
    }
    else
    {
      digitalWrite(HUMIDIFIER_PIN, LOW);
    }

    if(water_control == 1)
    {
      digitalWrite(PUMP_PIN, HIGH);
    }
    else
    {
      digitalWrite(PUMP_PIN, LOW);
    }
  }
  else
  {
    digitalWrite(FAN_PINA, LOW);
    digitalWrite(FAN_PINB, LOW);

    digitalWrite(FELTIER_PINA, LOW);
    digitalWrite(FELTIER_PINB, LOW);
    temperature_flag = 0;

    digitalWrite(HUMIDIFIER_PIN, LOW);
    humidity_flag = 0;

    digitalWrite(PUMP_PIN, LOW);
    water_flag = 0;
  }



  sendCurrentStatus();


}

