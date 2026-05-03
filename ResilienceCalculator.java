/**
 * ResilienceCalculator
 *
 * A small, strongly-typed engine for computing the Labour Stability Index (LSI)
 * and demonstrating the Ontario Economic Resilience model.
 */
public class ResilienceCalculator {

    // Small constant added to avoid division by zero when unemployment is extremely low.
    private static final double UNEMPLOYMENT_EPSILON = 0.1;

    /**
     * Calculates the Labour Stability Index (LSI).
     *
     * Formula:
     *   LSI = (EmploymentRate / (UnemploymentRate + 0.1)) * (ParticipationRate / 100)
     *
     * @param employmentRate   Employment rate (percentage, e.g., 60.0 for 60%)
     * @param unemploymentRate Unemployment rate (percentage, e.g., 7.7 for 7.7%)
     * @param participationRate Participation rate (percentage, e.g., 65.0 for 65%)
     * @return the calculated LSI as a double
     * @throws IllegalArgumentException if any rate is negative
     */
    public static double calculateLSI(double employmentRate,
                                      double unemploymentRate,
                                      double participationRate) {

        if (employmentRate < 0 || unemploymentRate < 0 || participationRate < 0) {
            throw new IllegalArgumentException("Rates must be non-negative.");
        }

        double adjustedUnemployment = unemploymentRate + UNEMPLOYMENT_EPSILON;
        double participationFactor = participationRate / 100.0;

        return (employmentRate / adjustedUnemployment) * participationFactor;
    }

    /**
     * Simple demo using Ontario 2025 data.
     */
    public static void main(String[] args) {
        double employmentRate = 60.0;
        double unemploymentRate = 7.7;
        double participationRate = 65.0;

        double lsi = calculateLSI(employmentRate, unemploymentRate, participationRate);

        System.out.printf("Ontario 2025 Labour Stability Index (LSI): %.4f%n", lsi);
    }
}
