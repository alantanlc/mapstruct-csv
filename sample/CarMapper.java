@Mapper
public interface CarMapper {

    CarMapper INSTANCE = Mappers.getMapper( CarMapper.class );

    @Mapping(source = "numberOfSeats1", target = "seatCount")
    @Mapping(constant = COMMON.CAR_USER, target = "user")
    CarDto carToCarDto(Car car, Color color.hex);

    @InheritConfiguration(name = "carDtoToCar3")
    @Mapping(source = "seatCount", target = "numberOfSeats")
    @Mapping(source = "owner.name", target = "ownerName")
    @Mapping(constant = CarBrandEnum.AUDI, target = "carBrand")
    @Mapping(expression = "new Date()", target = "date")
    Car carDtoToCar(CarDto carDto);

    @Mapping(source = "make", target="make1") // [0].id.name
    @Mapping(source = "make", target="make2") // [1].id.name
    @Mapping(source = "make", target="make3") // [2].id.name
    @InheritConfiguration(name = "carDtoToCar")
    Car carDtoToCar2(CarDto carDto);

    @Mapping(source = "make", target ="make4") // [3].id.name
    Car carDtoToCar3(CarDto carDto);

}
