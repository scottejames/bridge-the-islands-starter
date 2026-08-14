import java.io.IOException;

/** Demo runner — runs countReachableQueries on one example case and prints the result. */
public class Main {
    public static void main(String[] args) throws IOException {
        TestData.TestCase c = TestData.loadCase(TestData.TEST_DATA_DIR + "/medium/01_long_chain_trap.txt");

        System.out.println("Case: " + c.name);
        System.out.println("Islands: " + c.n);
        System.out.println("Events:");
        for (String event : c.events) {
            System.out.println("  " + event);
        }

        int result = BridgeIslands.countReachableQueries(c.n, c.events);
        System.out.println("Queries answered yes: " + result);
    }
}
