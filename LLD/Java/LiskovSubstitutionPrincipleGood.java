package Java;
public class LiskovSubstitutionPrincipleGood {
    public static void main (String[] args) {
        ComputerUpgrader upgrader = new ComputerUpgrader();
        DesktopComputer desktopPC = new DesktopComputer();
        Phone phone = new Phone();

        System.out.println("Before the OS update and RAM upgrade: ");
        printInfo(desktopPC, phone);

        upgrader.upgradeOS(desktopPC);
        upgrader.upgradeRAM(desktopPC);
        upgrader.upgradeOS(phone);
        // Following is not applicable
        // upgrader.upgradeRAM(phone);

        System.out.println("After the OS update and RAM upgrade: ");
        printInfo(desktopPC, phone);

    }

    static void printInfo(Computer desktopPC, Computer phone) {
        System.out.println("Desktop Computer has OS version: " + desktopPC.os_version + ", and amount of RAM: " +
                desktopPC.amount_of_ram + " GB.");
        System.out.println("Phone has OS version: " + phone.os_version + ", and amount of RAM: " + phone.amount_of_ram +
                " GB.");
    }
}


abstract class Computer {
	// Common properties (vars and funs) in all objects
    public int amount_of_ram = 4;
	public int os_version = 1;
	public abstract void updateOS();
}

class Phone extends Computer {
    // Can't upgradeRAM it so not written
	public void updateOS() {
		this.os_version += 1;
	}
}

class ComputerUpgrader {
    // Interface type passed as argument
    // If we need to implement upgradeRAM for any class that implements this interface
	public void upgradeRAM(HardwareUpgradable d) {
		d.addRam(16);
	}

	public void upgradeOS(Computer d) {
		d.updateOS();
	}
}

// Interface used for Hardware Upgradable devices!
interface HardwareUpgradable {
	void addRam(int gb);
}

class DesktopComputer extends Computer implements HardwareUpgradable {
    // Can upgrade RAM so we implement the interface!
	public void addRam(int gb) {
		this.amount_of_ram += gb;
	}

	public void updateOS() {
		this.os_version += 1;
	}
}

