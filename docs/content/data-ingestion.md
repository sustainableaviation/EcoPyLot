# Data Ingestion Pipeline

JSON file fomat is used to ingest data into EcoPyLot. The format of the input JSON file and the ouput DataFrame along with the Unique Dictionary ouput in specified below.

```{mermaid}
graph LR
    A[JSON Input] --> B[EcoPyLot]
    B --> C[Static DataFrame Output]
    B --> D[Stochastic DataFrame Output]
    C --> E[Unique Dictionary Output]
    D --> E
    style A fill:#f9d,stroke:#333,stroke-width:2px
    style B fill:#fc0,stroke:#333,stroke-width:2px
    style C fill:#9cf,stroke:#333,stroke-width:2px
    style D fill:#9cf,stroke:#333,stroke-width:2px
    style E fill:#9f9,stroke:#333,stroke-width:2px
```

## JSON Input

The JSON input is a dictionary where each key is a unique identifier (UID) for a set of parameters. Each UID maps to another dictionary containing the following keys:

- `parameter` (string): The parameter name.
- `year` (integer): The year.
- `fuselage` (string): The type of fuselage.
- `energy source` (string): The energy source.
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

### Example

Here is an example of a JSON input:

```json
{
    "<someJSON UID>": {
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
        "url":  "https://doi.org/10.1016/j.trd.2017.10.017",
        "comment": "for testing purposes only"
    }
}
```

## DataFrame Output
The output from EcoPyLot is a DataFrame, either a [Static DataFrame](#static-dataframe-output) or [Stochastic DataFrame](#stochastic-dataframe-output). In addition it also generates a [Unique Dictionary](#unique-dictionary-output) as output.


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