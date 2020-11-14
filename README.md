# MapStruct CSV

Parses a Java MapStruct interface file and generates a csv that can be pasted on a Confluence page.

## Dependencies

- python3+

## How to run

Run `mapper.py` using python3:
```
python3 mapper.py -f <path_to_file> -s <source_column_heading> -t <target_column_heading> [-r]
```

Example:
```
python3 mapper.py -f ./sample/CarMapper.java -s From -t To
```

Console output
```
Generated csv for ./sample/CarMapper.java:
  carToCarDto(Car_car) -> [carToCarDto(Car_car).csv]
  carDtoToCar(CarDto_carDto) -> [carDtoToCar(CarDto_carDto).csv]
```

## Reverse flag

Use `-r` flag to reverse order of columns in csv output:
```
python mapper.py -f ./sample/CarMapper.java -s From -t To -r
```

## Generated CSV

carToCarDto(Car_car,_Color_color.hex);.csv
```
TO,FROM
numberOfSeats,seatCount
```

carDtoToCar(CarDto_carDto);.csv
```
TO,FROM
seatCount,numberOfSeats
owner.name,ownerName
CarBrandEnum.AUDI,carBrand
new Date(),date
```

## How to paste generated csv on a confluence page

1. Open the confluence page in edit mode
1. Navigate 'Insert more content' > 'Other macros'
1. Search for 'csv'
1. Select 'Advanced Tables - CSV Table'
1. Leave CSV settings unchanged (Method of locating script should be 'None' and leave File encoding input empty)
1. Select 'Save settings'
1. An 'Advanced Tables - CSV Table' box is generated.
1. Copy and paste the generated csv text into the text area in the box.
1. Save page