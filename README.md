# 🚆 schiene
schiene is a Python library for interacting with Bahn.de. Consider it a unofficial API client. This library uses **realtime,  live** information retrieved from Bahn.de and therefore contains information on delays, cancellations etc.

[![Maintainability](https://api.codeclimate.com/v1/badges/972771137462082930b9/maintainability)](https://codeclimate.com/github/kennell/schiene/maintainability)

<sub>Note: if you do not need live information (delays etc.) you can use the new official [Fahrplan API](http://data.deutschebahn.com/apis/fahrplan/) from Deutsche Bahn. Also, the Bahn.de HTML code is a steaming pile of shit that can cause this library to break at any time. Do not use for any critical stuff.</sub>

<sub>schiene was built during a Hackday event at [PhraseApp](https://phraseapp.com)</sub>

## Install

```
pip install schiene
```

## Usage examples
```python
>>> import schiene
>>> s = schiene.Schiene()
>>> s.connections('Mannheim HbF', 'Stuttgart HbF')
[{'arrival': '13:08',
  'canceled': True,
  'delay' : {
    'delay_departure' : 15,
    'delay_arrival': 0
  }
  'departure': '12:30',
  'details': 'http://mobile.bahn.de/bin/mobil/query.exe/dox?ld=15085&n=1&i=or.0179785.1439546366&rt=1&use_realtime_filter=1&co=C0-1&vca&HWAI=CONNECTION$C0-1!details=opened!&',
  'price': 39.0,
  'products': ['ICE'],
  'time': '0:38',
  'transfers': 0},
 {'arrival': '13:54',
  'departure': '12:38',
  'details': 'http://mobile.bahn.de/bin/mobil/query.exe/dox?ld=15085&n=1&i=or.0179785.1439546366&rt=1&use_realtime_filter=1&co=C0-2&vca&HWAI=CONNECTION$C0-2!details=opened!&',
  'ontime': True,
  'price': 30.0,
  'products': ['S', 'EC'],
  'time': '1:16',
  'transfers': 1},
  ...]
>>> s.stations('Hamburg')
[{'extId': '008002549',
  'id': 'A=1@O=Hamburg '
        'Hbf@X=10006908@Y=53552732@U=80@L=008002549@B=1@p=1439332022@',
  'prodClass': '15',
  'state': 'id',
  'type': '1',
  'typeStr': '[Bhf/Hst]',
  'value': 'Hamburg Hbf',
  'weight': '24258',
  'xcoord': '10006908',
  'ycoord': '53552732'},
 {'extId': '008002548',
  'id': 'A=1@O=Hamburg '
        'Dammtor@X=9989568@Y=53560751@U=80@L=008002548@B=1@p=1439332022@',
  'prodClass': '31',
  'state': 'id',
  'type': '1',
  'typeStr': '[Bhf/Hst]',
  'value': 'Hamburg Dammtor',
  'weight': '27663',
  'xcoord': '9989568',
  'ycoord': '53560751'},
  ...]
```

## Projects using schiene

* [Home Assistant](https://github.com/home-assistant/home-assistant)
