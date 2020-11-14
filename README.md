# MapStruct Table

Parses a Java MapStruct interface file and generates a csv that can be pasted on a Confluence page.

## Dependencies

- python3+

## How to run

Run `mapper.py` using python3:
```python3
python3 mapper.py -f <path_to_file>
```

Example:
```python3
python3 mapper.py -f ./sample/CarMapper.java
```

Output:
```
Generated csv for ./sample/CarMapper.java:
  carToCarDto(Car_car) -> [carToCarDto(Car_car).csv]
  carDtoToCar(CarDto_carDto) -> [carDtoToCar(CarDto_carDto).csv]
```

## How to paste csv on a Confluence page

1. Open the confluence page in edit mode
1. Navigate 'Insert more content' > 'Other macros'
1. Search for 'csv'
1. Select 'Advanced Tables - CSV Table'
1. Leave CSV settings unchanged (Method of locating script should be 'None' and leave File encoding input empty)
1. Select 'Save settings'
1. Copy and paste the generate csv text into the 'Advanced Tables - CSV Table' text area