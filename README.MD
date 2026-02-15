# Terra Drive Web Socket 

TerraDrive.eu is able to connect to a webserver and streams real time car data
such as current position, speed, RPMs, gear, way point and more.
This allows you to create a fun projects such as custom speedometer, navigation and more.
Usage is very simple.

<img src="imgs/demo.gif" width="400"/>

## Quick start
1. Install requirements `pip install -r requirements.txt`
2. Start example `python examples/simple_speedometer.py`
3. Go to www.terradrive.eu and start open world game
4. Press"`" or  ";" key to open in game console
5. Type `/wsConnect localhost:8765`
6. You should see moving speedometer
7. Optional you can type `/wsDisconnect` to stop streaming data


## Data Sending
Data are send in JSON format.



| Name         | Attribute                        | Note                                                         |
|--------------|----------------------------------|--------------------------------------------------------------|
| speed        | current car speed                | speed in meter per second                                    |
| gear         | car gear                         | 0=R, 1=N, 2.. (`gear=v-1`, e.g. 2=first gear, 3=second gear) |
| rpm          | RPM                              | revolution per minute                                        |
| parkingBreak | parking break engaged            | true / false                                                 |
| light        | light mode                       | 0-off, 1-on                                                  |
| blinker      | blinker mode                     | 0-off, 1-left, 2-right, 3-all                                |
| fuel         | fuel meter                       | 0 = no fuel, 1=full tank                                     |
| pos          | Real world car pos               | lat, lon                                                     |
| inGamePos    | Car position in game coordinates | (x, y, z) , one unit=1m, y=altitude                          |
| heading      | car headiing                     | in degree, 0=North, 180 or -180 = South                      |
| odometer     | millage                          | odometer in meters                                           |
| navPoint     | navigation point                 | null if not set, else lat, lon in world coordiantes          |
| car          | car type                         | select car type e.g. fastCar, semiTruck                      |                     |

Example:

```JSON
{
  "speed":0,
  "gear":1,
  "rpm":800,
  "parkingBreak":false,
  "light":1,
  "blinker":0,
  "fuel":0.7262313424659486,
  "pos":{
    "lon":14.293547808222385,
    "lat":50.034694585520775
  },
  "inGamePos":
    [-390.1487590173294,332.188434167615,506.61860117799404],
  "heading":29.098252226960238,
  "car":"default",
  "odometer":550.6273852907253,
  "navPoint":{
    "lat":50.02475017960823,
    "lon":14.3013249098639
  }
}
```

## Start your project

If you want to start your project, I recommend use `td_ws_server.py` as a starting point.