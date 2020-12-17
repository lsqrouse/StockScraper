package me.quinnkump.app;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@SpringBootApplication
@Controller
public class StockScraperApplication {

	public static void main(String[] args) {
		SpringApplication.run(StockScraperApplication.class, args);
	}

	@GetMapping("/home")
	public String getHomePage(){
		return "home";
	}

}
