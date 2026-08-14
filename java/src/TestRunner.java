import java.io.IOException;
import java.util.List;

/**
 * Test harness for Bridge the Islands.
 *
 * Run all cases in ../test_data/{simple,medium,hard}/ against your
 * solution and report PASS/FAIL per case, per tier, and overall, with
 * timing. Exits with status 1 if any test fails.
 *
 * Simple and medium cases are small enough to trace by hand; hard cases
 * are larger generated cases intended to test how your solution scales,
 * not just whether it's correct. See ../test_data/README.md for details
 * on every case.
 */
public class TestRunner {

    private static final String[] TIERS = {"simple", "medium", "hard"};

    private static class TierResult {
        final int passed;
        final int failed;
        final double totalMs;

        TierResult(int passed, int failed, double totalMs) {
            this.passed = passed;
            this.failed = failed;
            this.totalMs = totalMs;
        }
    }

    public static void main(String[] args) throws IOException {
        int totalPassed = 0;
        int totalFailed = 0;
        TierResult hardResult = null;

        for (String tier : TIERS) {
            System.out.println("\n--- " + tier + " ---");
            TierResult result = runTier(tier);
            totalPassed += result.passed;
            totalFailed += result.failed;
            System.out.printf("%s: %d passed, %d failed, total %.1fms%n",
                    tier, result.passed, result.failed, result.totalMs);
            if (tier.equals("hard")) {
                hardResult = result;
            }
        }

        System.out.println();
        System.out.println("TOTAL: " + totalPassed + " passed, " + totalFailed + " failed out of "
                + (totalPassed + totalFailed));
        System.out.printf("Hard tier: %d/%d passed, %.1fms total%n",
                hardResult.passed, hardResult.passed + hardResult.failed, hardResult.totalMs);
        System.out.println("Efficiency band: "
                + efficiencyBand(hardResult.failed == 0, hardResult.totalMs));

        if (totalFailed > 0) {
            System.exit(1);
        }
    }

    private static String efficiencyBand(boolean hardAllPassed, double hardTotalMs) {
        if (!hardAllPassed) {
            return "N/A -- hard tier did not fully pass";
        }
        if (hardTotalMs < 2000) {
            return "Efficient (< 2s total)";
        }
        if (hardTotalMs < 10000) {
            return "Adequate (2-10s total)";
        }
        return "Slow (> 10s total) -- worth revisiting your approach";
    }

    private static TierResult runTier(String tier) throws IOException {
        List<TestData.TestCase> cases = TestData.loadTier(tier);
        int passed = 0;
        int failed = 0;
        double totalMs = 0;

        for (TestData.TestCase c : cases) {
            String status;
            String actualStr;
            long start = System.nanoTime();
            try {
                int actual = BridgeIslands.countReachableQueries(c.n, c.events);
                boolean ok = actual == c.expected;
                status = ok ? "PASS" : "FAIL";
                actualStr = String.valueOf(actual);
                if (ok) {
                    passed++;
                } else {
                    failed++;
                }
            } catch (UnsupportedOperationException e) {
                status = "FAIL";
                actualStr = "NOT IMPLEMENTED";
                failed++;
            }
            double elapsedMs = (System.nanoTime() - start) / 1_000_000.0;
            totalMs += elapsedMs;
            System.out.printf("[%s] %s/%s: expected=%d actual=%s (%.1fms)%n",
                    status, tier, c.name, c.expected, actualStr, elapsedMs);
        }

        return new TierResult(passed, failed, totalMs);
    }
}
