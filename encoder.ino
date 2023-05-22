#define outputXA 6
#define outputXB 7
#define outputYA 8
#define outputYB 9
long counter[2] = {0, 0};
int XAState, YAState;
int XLastState, YLastState;

void setup()
{
    pinMode(outputXA, INPUT);
    pinMode(outputXB, INPUT);
    pinMode(outputYA, INPUT);
    pinMode(outputYB, INPUT);
    Serial.begin(2000000);

    // Reads the initial state of the outputA
    XLastState = digitalRead(outputXA);
    YLastState = digitalRead(outputYA);
}

void loop()
{
    XAState = digitalRead(outputXA); // Reads the "current" state of the outputA
    YAState = digitalRead(outputYA);

    // If the previous and the current state of the outputA are different, that means a Pulse has occured
    if (XAState != XLastState)
    {
        // If the outputB state is different to the outputA state, that means the encoder is rotating clockwise
        if (digitalRead(outputXB) != XAState)
            counter[0]++;
        else
            counter[0]--;
    }

    // If the previous and the current state of the outputA are different, that means a Pulse has occured
    if (YAState != YLastState)
    {
        // If the outputB state is different to the outputA state, that means the encoder is rotating clockwise
        if (digitalRead(outputYB) != YAState)
            counter[1]++;
        else
            counter[1]--;
    }

    Serial.print(counter[0]);
    Serial.print(",");
    Serial.println(counter[1]);

    XLastState = XAState;
    YLastState = YAState; // Updates the previous state of the outputA with the current state
}