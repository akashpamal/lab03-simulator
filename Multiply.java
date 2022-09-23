public class Multiply {
    public static void main(String[] args) {
        int x = 10;
        int y = 9;
        int rolling_sum = 0;
        int index = 0;

        do {
            rolling_sum += x;
            index += 1;
        } while (index - y <= 0);
        rolling_sum -= x;
        System.out.println("Product: " + rolling_sum);
    }
}