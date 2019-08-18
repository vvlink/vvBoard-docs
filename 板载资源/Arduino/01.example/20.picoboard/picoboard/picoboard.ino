// DigitalSandboxPico
//
// PicoBoard Firmware modified for the DigitalSandBox 
// Arduino Learning Platform.
// Ported over from original C code.
//
// Modified by: Brian Huang, Sparkfun Electronics
// Date:  August 7, 2014

#define SCRATCH_DATA_REQUEST 0x01

char request = 0;
unsigned int sensor_value = 0;
char data_packet[2]= "";

int SLIDER = A3; // Slider on DS Board
int SOUND = A2;  // Microphone on DS Board
int LIGHT = A1;  // Light Detector on DS Board
int BUTTON = 12; // Push Button on DS Board

int RA = A0; // Temp
int RB = 2;  // Switch
int RC = 3;  // D3 -- Side Port 
int RD = A4; // A4 -- Top Port

void setup()
{
  pinMode(BUTTON, INPUT_PULLUP);  // enable internal pull-up resistor
  pinMode(RB, INPUT_PULLUP);  // enable internal pull-up resistor
  Serial.begin(38400);
}

void loop()
{
  request = Serial.read();
  if(request == SCRATCH_DATA_REQUEST)
  {
    // send the ID packet
    buildScratchPacket(data_packet, 15, 0x04);
    sendScratchPacket(data_packet);

    // Do not change the order of this sequence. Scratch expects the data 
    // to be organized in this order.

    //Read/Report channel 0 (Resistance-D)
    sensor_value=analogRead(RD);
    buildScratchPacket(data_packet, 0, sensor_value);
    sendScratchPacket(data_packet);

    //Read/Report Channel 1 (Resistance-C)
    sensor_value=analogRead(RC);
    buildScratchPacket(data_packet, 1, sensor_value);
    sendScratchPacket(data_packet);

    //Read/Report Channel 2 (Resistance-B)
    sensor_value=1023*digitalRead(RB);
    buildScratchPacket(data_packet, 2, sensor_value);
    sendScratchPacket(data_packet);         

    //Read/Report Channel 3 (Button)
    sensor_value = 1023*(1 - digitalRead(BUTTON));
    buildScratchPacket(data_packet, 3, sensor_value);
    sendScratchPacket(data_packet); 

    //Read/Report Channel 4(Resistance-A)
    sensor_value=analogRead(RA);
    buildScratchPacket(data_packet, 4, sensor_value);
    sendScratchPacket(data_packet);     

    //Read/Report Channel 5(LIGHT)
    sensor_value=1023 - analogRead(LIGHT);
    buildScratchPacket(data_packet, 5, sensor_value);
    sendScratchPacket(data_packet); 

    //Read/Report Channel 6(Sound)
    sensor_value=analogRead(SOUND);
    buildScratchPacket(data_packet, 6, sensor_value);
    sendScratchPacket(data_packet);         

    //Read/Report Channel 7(Slider)
    sensor_value=analogRead(SLIDER);
    buildScratchPacket(data_packet, 7, sensor_value);
    sendScratchPacket(data_packet);
  }
}

void buildScratchPacket(char * packet, int channel, int value)
{
  char upper_data=(char)((value&(unsigned int)0x380)>>7);   //Get the upper 3 bits of the value
  char lower_data=(char)(value&0x7f);   //Get the lower 7 bits of the value
  *packet++=((1<<7)|(channel<<3)|(upper_data));
  *packet++=lower_data;
}

void sendScratchPacket(char * packet)
{
  Serial.write(*packet++);
  delayMicroseconds(400);
  Serial.write(*packet++);
  delayMicroseconds(400);
}
