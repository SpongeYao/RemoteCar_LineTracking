#define MotorR_I1     8  //Define I1 PIN
#define MotorR_I2     9  //Define I2 PIN
#define MotorL_I3    10  //Define I3 PIN
#define MotorL_I4    11  //Define I4 PIN
#define MotorR_ENA    5  //Define ENA(PWM) PIN
#define MotorL_ENB    6  //Define ENB(PWM) PIN

//Global Variables
char cmd_byte= 0;
String cmd= "";
String a="";
boolean check_stop= true;

void setup()
{
  Serial.begin(115200); 
  
  pinMode(MotorR_I1,OUTPUT);
  pinMode(MotorR_I2,OUTPUT);
  pinMode(MotorL_I3,OUTPUT);
  pinMode(MotorL_I4,OUTPUT);
  pinMode(MotorR_ENA,OUTPUT);
  pinMode(MotorL_ENB,OUTPUT);
  
  analogWrite(MotorR_ENA,200);    //Set Right Motor Speed 
  analogWrite(MotorL_ENB,200);    //Set Left Motor Speed
}

void goStraight(int a)    // go forward
{
    digitalWrite(MotorR_I1,HIGH);   //Right Motor CW
    digitalWrite(MotorR_I2,LOW);
    digitalWrite(MotorL_I3,HIGH);   //Left Motor CCW
    digitalWrite(MotorL_I4,LOW);
    delay(a * 50);
}

void turnL(int d)    // turn Left
{
    digitalWrite(MotorR_I1,LOW);    
    digitalWrite(MotorR_I2,HIGH);
    digitalWrite(MotorL_I3,HIGH);  
    digitalWrite(MotorL_I4,LOW);
    delay(d * 50);
}

void turnR(int e)    // turn Right
{
    digitalWrite(MotorR_I1,HIGH); 
    digitalWrite(MotorR_I2,LOW);
    digitalWrite(MotorL_I3,LOW);   
    digitalWrite(MotorL_I4,HIGH);
    delay(e * 50);
}    

void stopRL(int f)  // Stop
{
    digitalWrite(MotorR_I1,HIGH); 
    digitalWrite(MotorR_I2,HIGH);
    digitalWrite(MotorL_I3,HIGH); 
    digitalWrite(MotorL_I4,HIGH);
    delay(f * 50);
}

void back(int g)    // go backward
{
    digitalWrite(MotorR_I1,LOW); 
    digitalWrite(MotorR_I2,HIGH);
    digitalWrite(MotorL_I3,LOW); 
    digitalWrite(MotorL_I4,HIGH);
    delay(g * 50);     
}

void loop()
{
  // Read serial input:
  while (Serial.available() > 0)
  {
    //cmd= Serial.readString();// read the incoming data as string
    Serial.print(">>> ");
    
    //Serial.println(cmd[0]); 
    String number="";
    /*
    for(int i=1;i<cmd.length();i++)
    {
      number= number+ String(cmd[i]);
    }
    //*/
    //number = String(cmd[1])+String(cmd[2]);
    //Serial.println(amount);
    //int cmd = Serial.read();  // read Blooth
    //*
    //cmd="NaN";
    cmd_byte = Serial.read();       // get the character
    Serial.println(cmd_byte);
    if (cmd_byte != '\n') {
      // a character of the string was received
      cmd += cmd_byte;
    }else{
      Serial.println(cmd);
        //*/
      int amount= cmd.substring(1,cmd.length()).toInt();
      char Index= cmd[0];
      Serial.print("Input: ");
      Serial.println(cmd);
      Serial.println(Index);
      
      switch(Index)  
      {
        case 'S':  // backward
          back(amount);
          check_stop= false;
          break;
     
        case 'A':  // Turn Left
          Serial.println("LEFT");
          turnL(amount);
          check_stop= false;
          break;
            
        case 'D':  // Turn Right
          Serial.println("RIGHT");
          turnR(amount);
          check_stop= false;
          break;
          
        case 'W':  // forward
          goStraight(amount);
          check_stop= false;
          break;
            
        case 'Q':  // STOP
          check_stop=true;
          //stopRL(amount);
          break;
          
        //default:
        //  goStraight(1);
      }
      stopRL(1);
      cmd = "";                // clear the string for reuse
      if(check_stop==true)
      {
        stopRL(amount);
      }
      /*
      else
      {
        goStraight(1);
        //check_stop=false;
      }
      */
    }
  }
  //*/
}
