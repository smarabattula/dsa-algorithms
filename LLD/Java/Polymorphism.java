package Java;

class Cake {
    public void make() {
        System.out.println("Making a generic cake.");
    }

    public void make(Cake c) {
        System.out.println("Making a cake from another cake.");
    }
}

class ChocolateCake extends Cake {
    @Override
    public void make() {
        System.out.println("Making a chocolate cake.");
    }

    @Override
    public void make(Cake c) {
        System.out.println("Making a chocolate cake from a generic cake.");
    }

    public void make(ChocolateCake c) {
        System.out.println("Making a chocolate cake from another chocolate cake.");
    }
}

class BirthdayCake extends ChocolateCake {
    @Override
    public void make() {
        System.out.println("Making a birthday cake with decorations.");
    }

    @Override
    public void make(Cake c) {
        System.out.println("Making a birthday cake from a generic cake.");
    }

    @Override
    public void make(ChocolateCake c) {
        System.out.println("Making a birthday cake from a chocolate cake.");
    }

    public void make(BirthdayCake c) {
        System.out.println("Making a birthday cake from another birthday cake.");
    }
}

public class Polymorphism {
    public static void main(String[] args) {

    Cake          c  = new Cake();
    Cake          c1 = new ChocolateCake();
    ChocolateCake c2 = new ChocolateCake();
    Cake          c3 = new BirthdayCake();
    ChocolateCake c4 = new BirthdayCake();
    BirthdayCake  c5 = new BirthdayCake();

    // ArrayList<Cake> arr = new ArrayList<Cake>();
    // arr.add(c);
    // arr.add(c1);
    // arr.add(c2);
    // arr.add(c3);
    // arr.add(c4);
    // arr.add(c5);

    // c5.make(c5);
    // for (int i = 5; i < arr.size(); i ++){
    //     Cake a = arr.get(i);
    //     System.out.println(a);
    //     for (int j = 0; j < arr.size(); j++){
    //     Cake b = arr.get(j);
    //     System.out.println(String.format("%d, %d", i, j));
    //      a.make(b);
    //     }
    // }
    }

}
