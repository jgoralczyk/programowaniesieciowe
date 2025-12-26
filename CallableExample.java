import java.util.Random;
import java.util.concurrent.Callable;

public class CallableExample implements Callable<Integer> {

    @Override
    public Integer call() throws Exception {
        String w = Thread
        int number = 0;
        Random rand = new Random();
        for(int i = 0; i<6; i++){
            System.out.println("Losowanie" + i);
            number += rand.nextInt(300,450);
            try {
                Thread.sleep(rand.nextInt(900, 4500));
            } catch (InterruptedException e){
                throw new RuntimeException(e);
            }
        }
 //       System.out.println("Wylosowana liczba: " + number);
        System.out.println("Zakonczenie pracy watka");
        return number;
    }
}
