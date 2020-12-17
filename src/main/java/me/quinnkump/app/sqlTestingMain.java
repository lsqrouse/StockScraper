package me.quinnkump.app;

import me.quinnkump.app.MySQLAccess;

public class sqlTestingMain {
    public static void main(String[] args) throws Exception {
        MySQLAccess dao = new MySQLAccess();
        dao.readDataBase();
    }

}