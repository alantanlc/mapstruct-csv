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
