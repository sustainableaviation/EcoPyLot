# Program Structure

## Input Data

_EcoPylot_ calculates the environmental impact of aircraft based on a set of parameters that describe the aircraft. Some of these parameters are the different aircraft sub-efficiencies, the number of seats per aircraft, etc. Each parameter is associated with a set of aircraft metadata, such as the year of production, fuselage type, energy source, etc:

### Parameters and Metadata

- `parameter` (string): The parameter name.

- `year` (integer): The year of production.
- `fuselage` (string): The type of fuselage (TW, BWB, SBW, etc.).
- `energy source` (string): The energy source (H2, Battery, Kerosene, etc.).
- `energy conversion` (string): The energy conversion method.
- `Transmission` (string): The transmission type.
- `Propulsor` (string): The propulsor type.
- `Drag Reduction` (string): The drag reduction method.
- `sizes` (array of strings): A list of sizes.
- `amount` (integer): The amount.
- `loc` (integer): The location.
- `minimum` (integer): The minimum value.
- `maximum` (integer): The maximum value.
- `kind` (string): The kind of distribution.
- `uncertainty_type` (integer): The uncertainty type.
- `source` (string): The source of the data.
- `url` (string): The URL of the source.
- `comment` (string): Any additional comments.

`parameters` and `metadata` are ingested into _EcoPyLot_ from a JSON file. This JSON data is then transformed by _EcoPyLot_ to a tabulated format and stored as a [Pandas DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html).

### JSON Input Schema

The input file must be formatted in accordance with [JSON syntax](https://www.json.org/json-en.html). An example `parameter`/`metadata` pair:

```json
{
    "seats_2050_test": {
        "parameter": "seats",
        "year": 2050,
        "fuselage": "TW",
        "energy source": [
            "H2",
            "Battery"
        ],
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
        "amount": 150,
        "loc": 150,
        "minimum": 50,
        "maximum": 200,
        "kind": "distribution",
        "uncertainty_type": 5,
        "source": "Cox et al. (2018)",
        "url":  "https://doi.org/10.1016/j.trd.2017.10.017",
        "comment": "Test entry only!"
    }
}
```

## Tabulated Data

### Static DataFrame Output

In the static case, the DataFrame output is a table where each row corresponds to a unique identifier (UID) from the JSON input. The columns of the DataFrame correspond to the keys in the JSON input. The `amount` for each size is the same.

Example:

| UID | parameter | year | fuselage | ... | sizes | amount | source | url | comment |
| --- | --------- | ---- | -------- | --- | ----- | ------ | ------ | --- | ------- |
| h32497sdf8 | seats | 2000 | TW | ... | Commuter | 75 | Cox et al. (2018) | https://doi.org/10.1016/j.trd.2017.10.017 | for testing purposes only |
| h3249734f8 | seats | 2000 | TW | ... | Regional | 75 | Cox et al. (2018) | https://doi.org/10.1016/j.trd.2017.10.017 | for testing purposes only |

### Stochastic DataFrame Output

In the stochastic case, the DataFrame output is similar to the static case, but the `amount` for each size can vary.

Example:

| UID | parameter | year | fuselage | ... | sizes | amount | source | url | comment |
| --- | --------- | ---- | -------- | --- | ----- | ------ | ------ | --- | ------- |
| h32497sdf8 | seats | 2000 | TW | ... | Commuter | 25 | Cox et al. (2018) | https://doi.org/10.1016/j.trd.2017.10.017 | for testing purposes only |
| h3249734f8 | seats | 2000 | TW | ... | Commuter | 65 | Cox et al. (2018) | https://doi.org/10.1016/j.trd.2017.10.017 | for testing purposes only |
| h32497sdf8 | seats | 2000 | TW | ... | Regional | 85 | Cox et al. (2018) | https://doi.org/10.1016/j.trd.2017.10.017 | for testing purposes only |
| h3249734f8 | seats | 2000 | TW | ... | Regional | 75 | Cox et al. (2018) | https://doi.org/10.1016/j.trd.2017.10.017 | for testing purposes only |

## Unique Dictionary Output

In addition to the DataFrame, a dictionary of unique values for each parameter is also returned. This dictionary has each parameter as a key, and the unique values for that parameter as the values.

Example:

```python
unique_dict = {
    "parameters": ["seats", "year", "fuselage", ...],
    "fuselage": ["TW", "LW", ...],
    ...
}