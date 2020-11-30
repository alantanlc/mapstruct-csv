# MapStruct CSV

Parses a Java MapStruct interface file and generates CSV that can be pasted on confluence pages

## Dependencies

- python3+
- virtualenv
- pip3
- yaml

## Virtualenv and pip

Create a virtualenv directory:
```
virtualenv env
```

Activate environment (macOS/Linux):
```
source env/bin/activate
```

Activate environment (Windows):
```
.\env\bin\activate.bat
```

Install python packages using pip:
```
pip install -r requirements.txt
```

## How to run

Run `mapper-csv.py` using python3:
```
python3 mapper-csv.py -f <path_to_file> -s <source_column_heading> -t <target_column_heading> -d -r -c -i -j
```

Example:
```
python3 mapper-csv.py -f ./sample/CarMapper.java -s FROM -t TO -d -r -c -i -j
```

Console output
```
Generated csv for ./sample/CarMapper.java:
  getMapper(_CarMapper.class_); -> [output/getMapper(_CarMapper.class_);.csv]
  carToCarDto(Car_car,_Color_color.hex); -> [output/carToCarDto(Car_car,_Color_color.hex);.csv]
  carDtoToCar(CarDto_carDto); -> [output/carDtoToCar(CarDto_carDto);.csv]
  carDtoToCar2(CarDto_carDto); -> [output/carDtoToCar2(CarDto_carDto);.csv]
  carDtoToCar3(CarDto_carDto); -> [output/carDtoToCar3(CarDto_carDto);.csv]
```

## Argparse

Run `python3 mapper-csv.py -h` to display argparse options:
```
usage: mapper-csv.py [-h] [-y YAML] [-f FILENAME] [-s SOURCE] [-t TARGET] [-d] [-r] [-c [COMMENT]] [-i] [-j] [-o OUTPUT]

Parses a Java MapStruct interface file and generates CSV that can be pasted on confluence pages

optional arguments:
  -h, --help            show this help message and exit
  -y YAML, --yaml YAML  name of yaml config file
  -f FILENAME, --filename FILENAME
                        name of mapper interface file
  -s SOURCE, --source SOURCE
                        heading text of source column
  -t TARGET, --target TARGET
                        heading text of target column
  -d, --database        format target names as database column names
  -r, --reverse         reverse the column output order
  -c [COMMENT], --comment [COMMENT]
                        include a comment column at the end
  -i, --inherit         include @InheritConfiguration mappings
  -j, --join            join source with additional mapping defined as a comment on the same line
  -o OUTPUT, --output OUTPUT
                        name of output directory
```

## Generated CSV

carToCarDto(Car_car,_Color_color.hex);.csv
```
TO,FROM,COMMENT
SEAT_COUNT,numberOfSeats1,
USER,COMMON.CAR_USER,
```

carDtoToCar(CarDto_carDto);.csv
```
TO,FROM,COMMENT
NUMBER_OF_SEATS,seatCount,
OWNER_NAME,owner.name,
CAR_BRAND,CarBrandEnum.AUDI,
DATE,new Date(),
MAKE4,make[3].id.name,
```

## How to paste generated csv on a confluence page as a normal table

1. Open generated csv using Microsoft Excel
1. Copy rows and columns
1. Open confluence page in edit mode and paste
1. Unsplit cells if necessary
1. Add heading rows and numbering columns if necessary
1. Save page and review output

## How to paste generated csv on a confluence page as an Advanced CSV Table

1. Open confluence page in edit mode
1. Navigate to 'Insert more content' > 'Other macros'
1. Search for 'csv'
1. Select 'Advanced Tables - CSV Table'
1. Leave CSV settings unchanged _(Method of locating script should be 'None' and leave File encoding input empty)_
1. Select 'Save settings'
1. An 'Advanced Tables - CSV Table' box is generated
1. Copy and paste the generated csv text into the text area in the box
1. Save page and review output
