package Java;
// Given to construct a pizza building API

// Step 1: Requirements
// Pizza: 1 base, 1 size, 0 to n toppings
// Price Calculation:
// Each base has it's own price
// Size has a base price, and a multiplier added at the end
// Topping has it's own price, name
// Implement

// Step 2: Implementation
// Have multiple customizations, so b x s x t pizza combinations!
// 1) Pizza (String base, int size, List <String> toppings)
// 2) Pizza constructors for all topping combinations!

// abstract classes for bases, sizes, toppings
// Write concrete classes to extend abstract classes
// Write a Pizza class to encapsulate objects - size, base and toppings. Also their methods to edit, add, delete can be fixated
// Use Pizza building class to building customized pizzas

// If predefined pizzas (Margeritha (cheese base, no toppings), Chicken pizza (Regular base, Chicken topping)), write an interface builder (instad of class!), and let individual builder class implement it
import java.util.*;

// Classes for BASE, SIZE, TOPPINGS
abstract class Base {
    protected String name;
    protected double price;

    public String getName() {
        return name;
    }

    public double getPrice() {
        return price;
    }
}

class RegularBase extends Base {
    public RegularBase() {
        this.name = "Regular Base";
        this.price = 2.0;
    }
}

class CheeseBase extends Base {
    public CheeseBase() {
        this.name = "Premium Base";
        this.price = 5.0;
    }
}

abstract class Size{
    protected int size;
    protected String name;
    protected double multiplier;

    public String getName() {
        return name;
    }

    public int getSize() {
        return size;
    }

    public double getMultiplier() {
        return multiplier;
    }
}

class SmallSize extends Size {
    public SmallSize(){
        this.size = 12;
        this.name = "Small 12 inch";
        this.multiplier = 1;
    }
}

class LargeSize extends Size {
    public LargeSize(){
        this.size = 18;
        this.name = "Large 18 inch";
        this.multiplier = 1.5;
    }
}

abstract class Topping{
    protected String name;
    protected double price;

    public String getName() {
        return name;
    }

    public double getPrice() {
        return price;
    }
}

class OnionTopping extends Topping{
    public OnionTopping(){
        this.name = "Onion";
        this.price = 0.5;
    }
}

class MushroomTopping extends Topping{
    public MushroomTopping(){
        this.name = "Mushroom";
        this.price = 0.75;
    }
}

class ChickenTopping extends Topping{
    public ChickenTopping(){
        this.name = "Chicken";
        this.price = 1;
    }
}

// Strategy Pattern for Price Calculation
interface PriceCalculator{
    public abstract double calculatePrice(Pizza p);
}

class RegularCalculator implements PriceCalculator{
    public double calculatePrice(Pizza p) {
        double totalPrice = 0;
        totalPrice += p.getBase().getPrice();
        for (Topping t: p.getToppings()){
            totalPrice += t.getPrice();
        }
        totalPrice *= p.getSize().getMultiplier();
        return totalPrice;
    }
}

class DiscountPercentCalc implements PriceCalculator{
    public int discountPercent;

    public DiscountPercentCalc(int discountPercent){
    this.discountPercent = discountPercent;
    }

    public double calculatePrice(Pizza p) {
        double totalPrice = 0;
        totalPrice += p.getBase().getPrice();
        for (Topping t: p.getToppings()){
            totalPrice += t.getPrice();
        }
        totalPrice *= p.getSize().getMultiplier();
        return totalPrice * discountPercent / 100;
    }
}

// Pizza class
class Pizza{
    private Base base;
    private Size size;
    private List<Topping> toppings = new ArrayList<>();
    private PriceCalculator pc;

    public Pizza() {}

    public Pizza(Base b, Size s, List<Topping> t, PriceCalculator pc){
        this.base     = b;
        this.size     = s;
        this.toppings = t;
        this.pc       = pc;
    }

    public Base getBase(){
        return this.base;
    }

    public Size getSize(){
        return this.size;
    }

    public List<Topping> getToppings(){
        return this.toppings;
    }

    public PriceCalculator getPriceCalculator(){
        return this.pc;
    }

    public double getPrice(){
        return this.pc.calculatePrice(this);
    }

    public void setBase(Base b){
        this.base = b;
    }

    public void setSize(Size s){
        this.size = s;
    }

    public void setPriceCalculator(PriceCalculator pc){
        this.pc = pc;
    }

    public void addTopping(Topping t){
        toppings.add(t);
    }

    public void removeTopping(String toppingName) {
    for (int i = 0; i < toppings.size(); i++) {
        if (toppings.get(i).getName().equalsIgnoreCase(toppingName)) {
            toppings.remove(i);
            break;
            }
        }
    }

}

// Builder pattern for Customized Pizza
class PizzaBuilder {
    private Pizza p;

    public PizzaBuilder(){
        this.p = new Pizza();
        this.p.setPriceCalculator(new RegularCalculator());

    }
    public PizzaBuilder setBase(Base b){
        p.setBase(b);
        return this;
    }

    public PizzaBuilder setSize(Size s){
        p.setSize(s);
        return this;
    }

    public PizzaBuilder setPriceCalculator(PriceCalculator pc){
        p.setPriceCalculator(pc);
        return this;
    }

    public PizzaBuilder addTopping(Topping t){
        p.addTopping(t);
        return this;
    }

    public PizzaBuilder removeTopping(String t){
        p.removeTopping(t);
        return this;
    }

    public Pizza build(){
        return new Pizza(p.getBase(), p.getSize(), p.getToppings(), p.getPriceCalculator());
    }
}

public class PizzaBuilding{
public static void main(String[] args){
    PizzaBuilder pb = new PizzaBuilder();
    Pizza p = pb.setSize(new LargeSize())
                      .setBase(new CheeseBase())
                      .addTopping(new ChickenTopping())
                      .addTopping(new OnionTopping())
                      .setPriceCalculator(new DiscountPercentCalc(20))
                      .build();

    // p.setBase(new RegularBase());
    System.out.println(p.getPrice());
    }
}
