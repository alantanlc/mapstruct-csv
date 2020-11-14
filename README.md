# MapStruct CSV

Parses a Java MapStruct interface file and generates CSV that can be pasted on confluence pages

## Dependencies

- python3+

## How to run

Run `mapper.py` using python3:
```
python3 mapper.py -f <path_to_file> -s <source_column_heading> -t <target_column_heading> [-r] [-d]
```

Example:
```
python3 mapper.py -f ./sample/CarMapper.java -s FROM -t TO
```

Console output
```
Generated csv for ./sample/CarMapper.java:
  carToCarDto(Car_car,_Color_color.hex); -> [carToCarDto(Car_car,_Color_color.hex);.csv]
  carDtoToCar(CarDto_carDto); -> [carDtoToCar(CarDto_carDto);.csv]
```

## Flags

Use `-r` flag to reverse the order of columns in csv output:
```
python mapper.py -f ./sample/CarMapper.java -s FROM -t TO -r
```

Use `-d` flag to format target names as database column names:
```
python mapper.py -f ./sample/CarMapper.java -s FROM -t TO -d
```

## Generated CSV

carToCarDto(Car_car,_Color_color.hex);.csv
```
TO,FROM
SEAT_COUNT,numberOfSeats1
```

carDtoToCar(CarDto_carDto);.csv
```
TO,FROM
NUMBER_OF_SEATS,seatCount
OWNER_NAME,owner.name
CAR_BRAND,CarBrandEnum.AUDI
DATE,new Date()
```

## How to paste generated csv on a confluence page

1. Open confluence page in edit mode
1. Navigate to 'Insert more content' > 'Other macros'
1. Search for 'csv'
1. Select 'Advanced Tables - CSV Table'
1. Leave CSV settings unchanged _(Method of locating script should be 'None' and leave File encoding input empty)_
1. Select 'Save settings'
1. An 'Advanced Tables - CSV Table' box is generated
1. Copy and paste the generated csv text into the text area in the box
1. Save page and review output