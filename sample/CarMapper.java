@Mapper
public interface CarMapper {

    CarMapper INSTANCE = Mappers.getMapper( CarMapper.class );

    @Mapping(source = "numberOfSeats1", target = "seatCount")
    @Mapping(constant = COMMON.CAR_USER, target = "user")
    CarDto carToCarDto(Car car, Color color.hex);

    @Mapping(source = "seatCount", target = "numberOfSeats")
    @Mapping(source = "owner.name", target = "ownerName")
    @Mapping(constant = CarBrandEnum.AUDI, target = "carBrand")
    @Mapping(expression = "new Date()", target = "date")
    Car carDtoToCar(CarDto carDto);

}
