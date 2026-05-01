public class ResilienceCalculator {
    /**
     * Calculates the Labour Stability Index of Ontario (LSI)
     * Formula: (Employment / (Unemployment + 0.1)) * (Participation / 100)
     */
    public static double calculateLSI(double empRate, double unempRate, double partRate) {
        // Adding 0.1 to avoid division by zero
        return (empRate / (unempRate + 0.1)) * (partRate / 100.0);
    }

    public static void main(String[] args) {
        // Testing with Ontario 2025 Data
        double emp = 60.0;
        double unemp = 7.7;
        double part = 65.0;

        double score = calculateLSI(emp, unemp, part);
        System.out.printf("The Calculated Resilience Score is: %.4f%n", score);
    }
}
