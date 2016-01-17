/*-----( Import needed libraries )-----*/
#include <Wire.h>  // Comes with Arduino IDE
// Get the LCD I2C Library here: 
// https://bitbucket.org/fmalpartida/new-liquidcrystal/downloads
// Move any other LCD libraries to another folder or delete them
// See Library "Docs" folder for possible commands etc.
#include <LiquidCrystal_I2C.h>
#include <ArduinoJson.h>

/*-----( Declare Constants )-----*/
/*-----( Declare objects )-----*/
// set the LCD address to 0x27 for a 16 chars 2 line display
// A FEW use address 0x3F
// Set the pins on the I2C chip used for LCD connections:
//                    addr, en,rw,rs,d4,d5,d6,d7,bl,blpol
LiquidCrystal_I2C lcd(0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);  // Set the LCD I2C address

String tweet1 = "{\"title\":\"@KieganB\",\"message\":\"Short tweet.\"}";
String tweet2 = "{\"title\":\"@LauraE\",\"message\":\"I love anime. I love sewing. I love video games. I love cats. I love porn.\"}";
String tweet3 = "{\"title\":\"@StephenL\",\"message\":\"A horse is a horse, of course, of course\"}";
String tweets[] = { tweet1, tweet2, tweet3 };

const int LINE_SIZE = 20; // maximum number of message characters per display line
const int DISPLAY_LINES = 4; // number of lines of the display can show
const int MAX_CHARS = LINE_SIZE * (DISPLAY_LINES-1); // maximum number of message characters that can be displayed at once

void setup()   /*----( SETUP: RUNS ONCE )----*/
{
  lcd.begin(LINE_SIZE,DISPLAY_LINES);  
  lcd.backlight();
  
}


void loop()   /*----( LOOP: RUNS CONSTANTLY )----*/
{
  for (int i=0; i<3; i++){
    StaticJsonBuffer<200> jsonBuffer;
    JsonObject& message = jsonBuffer.parseObject(tweets[i]);
    if (!message.success()) {
        lcd.write("Could not parse JSON");
        delay(3000);
        lcd.clear();
        continue;
    }
    
    String title = String((const char*)message["title"]);
    String text = String((const char*)message["message"]);

    int numLines = (text.length()/LINE_SIZE);
    if ((text.length() % LINE_SIZE) > 1){
      numLines++;
    }
    
    if (text.length() > MAX_CHARS){
      for(int t=0; t<2; t++){
        for(int i=0;(i+(DISPLAY_LINES-1))<=numLines; i++){
          lcd.setCursor(0,0);
          lcd.write(title.c_str());
          for(int j=0; j<(DISPLAY_LINES-1); j++){
             lcd.setCursor(0,(j+1));
             String line=text.substring((j+i)*LINE_SIZE,(j+i+1)*LINE_SIZE);   
             lcd.write(line.c_str());
          }
          delay(2000);        
          lcd.clear();
        }
      }
    }
    
    else {
      lcd.setCursor(0,0);
      lcd.write(title.c_str());
      for(int i=0; i<numLines; i++){
        lcd.setCursor(0,(i+1));
        String line=text.substring(i*LINE_SIZE,(i+1)*LINE_SIZE);
        lcd.write(line.c_str());
      }
      delay(5000);
      lcd.clear();    
    }
  }
}
/*
  {
    // when characters arrive over the serial port...
    if (Serial.available()) {
      // wait a bit for the entire message to arrive
      delay(100);
      // clear the screen
      lcd.clear();
      // read all the available characters
      while (Serial.available() > 0) {
        // display each character to the LCD
        lcd.write(Serial.read());
      }
    }
  }*/
