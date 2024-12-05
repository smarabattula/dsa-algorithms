package Java;
/*
Hotel management
-> Hotel has Rooms of different types
-> Room has id, isChecked, price

-> Reservation can be made on rooms
-> Reservation has id, customer, checkInTime, checkOutTime
-> Reservation has price calculation logic

-> Customer can make Reservations
-> Customer can edit/cancel Reservations
-> Customer can pay via various Payment modes

-> Manager can create/edit Room

 */
import java.time.LocalDateTime;

abstract class Room{
    protected String id;
    protected boolean isChecked;

    protected Room(String id){
        this.id = id;
        this.isChecked = false;
    }

    public String getId() {
        return id;
    }

    public boolean IsChecked() {
        return isChecked;
    }

    public void CheckIn() {
        if(this.isChecked){
            throw new IllegalStateException("Room already booked!");
        }
        this.isChecked = true;
    }

    public void CheckOut() {
        if(!this.isChecked){
            throw new IllegalStateException("Room not booked!");
        }
        this.isChecked = false;
    }

    public abstract double getPrice();
}

class StandardRoom extends Room{
    private static double price = 100.0;

    public StandardRoom(String id){
        super(id);
    }

    @Override
    public double getPrice() {
        return price;
    }
}

class DeluxeRoom extends Room{
    protected static double price = 150.0;
    public DeluxeRoom(String id){
        super(id);
    }

    @Override
    public double getPrice() {
        return price;
    }
}

class SuiteRoom extends Room{
    protected static double price = 200.0;
    public SuiteRoom(String id){
        super(id);
    }

    @Override
    public double getPrice() {
        return price;
    }
}

enum RoomType {
    STANDARD,
    SUITE,
    DELUXE
}

class RoomFactory {
    public Room createRoom(RoomType roomType, String id, double price) {
        switch (roomType) {
            case STANDARD:
                return new StandardRoom(id);
            case SUITE:
                return new SuiteRoom(id);
            case DELUXE:
                return new DeluxeRoom(id);
            default:
                throw new IllegalArgumentException("Invalid room type: " + roomType);
        }
    }
}

class Customer{
    private final String id;
    private String name;
    private String address;
    private String phone;
    private String email;

    public Customer(String id, String name, String address, String phone, String email){
        this.id = id;
        this.name = name;
        this.address = address;
        this.phone = phone;
        this.email = email;
    }

    public String getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }
}

enum BookingStatus{
    CONFIRMED,
    CANCELLED
    // UNPAID,
    // PAID
}
class Booking{
    private final String id;
    private final Customer customer;
    private final Room room;
    private BookingStatus status;
    private final LocalDateTime checkInTime;
    private LocalDateTime checkOutTime;

    public Booking(String id, Customer customer, Room room, LocalDateTime checkIn, LocalDateTime checkOut){
        this.id = id;
        this.customer = customer;
        this.checkInTime = checkIn;
        this.checkOutTime = checkOut;
        this.room = room;
        this.status = BookingStatus.CONFIRMED;
    }

    public String getId() {
        return id;
    }

    public Customer getCustomer() {
        return customer;
    }

    public LocalDateTime getCheckIn() {
        return checkInTime;
    }

    public LocalDateTime getCheckOut() {
        return checkOutTime;
    }

    public Room getRoom() {
        return room;
    }

    public void cancelBooking() {
        status = BookingStatus.CANCELLED;
    }

    public void CheckOut(){
        checkOutTime = LocalDateTime.now();

        // Write payment logic based on checkIn and checkOut

        // Update status based on payment status
    }

    public BookingStatus getStatus() {
        return status;
    }

}
/*
class RoomManager{
    private static Map <String, Room> rooms = new HashMap<>();

        public Map<String, Room> getRooms() {
            return rooms;
        }

        public void addRoom(Room room) {
            rooms.put(room.getId(), room);
    }

    public void removeRoom(String id){
        rooms.remove(id);
    }
}
*/

public class HotelManagement {
    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}
