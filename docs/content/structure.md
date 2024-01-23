# Structure


@iamsiddhantsahu: please update the below into a well-formated, well-explained documentation section.

```json
"<someDJSON UID>": {
    "parameter": "seats",
    "year": 2000,
    "fuselage": "TW",
    "energy source": "H2",
    "energy conversion": "FC",
    "Transmission": "Elec",
    "Propulsor": "Prop",
    "Drag Reduction": "None",
    "sizes": [
        "Commuter",
        "Regional",
        "Small Narrow Body",
        "Large Narrow Body",
        "Small Wide Body",
        "Large Wide Body"
    ],
    "amount": 75,
    "loc": 75,
    "minimum": 50,
    "maximum": 100,
    "kind": "distribution",
    "uncertainty_type": 5,
    "source": "Cox et al. (2018)",
    "url":  "https://doi.org/10.1016/j.trd.2017.10.017"
    "comment": "for testing purposes only"
},
```

df1 = ep.read_json("test.json")

xarray1 = carmodel(type=static)

xarray2 = carmodel(type=stochastic, sample_size=2)

in the STATIC case:

| UID | parameter | year | fuselage | ... | sizes | amount | source | url | comment |
| --- | --------- | ---- | -------- | --- | ----- | ------ | ------ | --- | ------- |
| h32497sdf8 | seats | 2000 | TW | ... | Commuter | 75 | Cox et al. (2018) | https://doi.org/10.1016/j.trd.2017.10.017 | for testing purposes only |
| h3249734f8 | seats | 2000 | TW | ... | Regional | 75 | Cox et al. (2018) | https://doi.org/10.1016/j.trd.2017.10.017 | for testing purposes only |

in the STOCHASTIC (sample_size=2) case:


| UID | parameter | year | fuselage | ... | sizes | amount | source | url | comment |
| --- | --------- | ---- | -------- | --- | ----- | ------ | ------ | --- | ------- |
| h32497sdf8 | seats | 2000 | TW | ... | Commuter | 25 | Cox et al. (2018) | https://doi.org/10.1016/j.trd.2017.10.017 | for testing purposes only |
| h3249734f8 | seats | 2000 | TW | ... | Commuter | 65 | Cox et al. (2018) | https://doi.org/10.1016/j.trd.2017.10.017 | for testing purposes only |
| h32497sdf8 | seats | 2000 | TW | ... | Regional | 85 | Cox et al. (2018) | https://doi.org/10.1016/j.trd.2017.10.017 | for testing purposes only |
| h3249734f8 | seats | 2000 | TW | ... | Regional | 75 | Cox et al. (2018) | https://doi.org/10.1016/j.trd.2017.10.017 | for testing purposes only |

What should also be returned:

unique_dict = {
    parameters: [seats, year, fuselage, ...],
    fuselage: [TW, LW, ...],
    ...
}