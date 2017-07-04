//Include libraries
#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire is plugged into pin 2 on the Arduino
#define ONE_WIRE_BUS 2
// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);
// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);

float values[10];
int valuesSize = 0;

void setup(void)
{
  Serial.begin(9600); //Begin serial communication
  sensors.begin();
  valuesSize = sizeof(values) / sizeof(float);
  for(int i = 0; i < valuesSize; i++)
  {
    values[i] = -99999;
  }
}

void loop(void)
{ 
  // Send the command to get temperatures
  sensors.requestTemperatures();

  // Why "byIndex"? You can have more than one IC on the same bus. 0 refers to the first IC on the wire
  values[0] = sensors.getTempCByIndex(0);
  values[1] = sensors.getTempCByIndex(1);

  // check for input on serial port
  if (Serial.available() > 0) {
    // read the input
    int inByte = Serial.read();
    //delay(500); // small delay before responding

    // respond only if correct command is received
    if ((char)inByte == 'r') {
      // respond with analog measurement
      for(int i = 0; i < valuesSize; i++)
      {
        //if value is set write it to the serial W
        if( values[i] != -99999)
        {
          Serial.println(values[i], DEC);
        }
      }
      
    }
  }
  
  delay(1000);
}
