package me.quinnkump.app;

import me.quinnkump.app.MySQLAccess;

import java.util.ArrayList;

public class sqlTestingMain {
    public static void main(String[] args) throws Exception {
        //MySQLAccess dao = new MySQLAccess();
        //dao.readDataBase();
        ArrayList<String> tickers = parseTickers("$CRSR part 2");
        for (String s: tickers) {
            System.out.printf("Found Ticker %s\n", s);
        }
    }

    public static ArrayList<String> parseTickers(String text) {
        ArrayList<String> tickers = new ArrayList<>();
        for (int i = 0; i < text.length(); i++) {
            if (text.charAt(i) == '$') {
                int j = i + 1;
                //we found a new ticker, build the string
                while (j < text.length() && isLetter(text.charAt(j))) {
                    j++;
                }
                String s = text.substring(i + 1, j);
                if (!s.equals("")) {
                    tickers.add(s);
                }
                i = j;
            }
        }
        return tickers;
    }

    public static boolean isLetter(char c) {
        return ((c > 64 && c < 91) || (c > 97 && c <123));
    }

}