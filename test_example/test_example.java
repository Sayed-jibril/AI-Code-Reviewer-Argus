import java.sql.*;
import java.security.MessageDigest;

public class BadClass {
    private String apiKey = "sk-1234567890abcdef"; // Hardcoded secret
    
    public void badMethod(String userInput) {
        try {
            Connection conn = DriverManager.getConnection("jdbc:mysql://localhost/db");
            Statement stmt = conn.createStatement();
            
            // SQL concatenation (injection risk)
            String query = "SELECT * FROM users WHERE id = " + userInput;
            ResultSet rs = stmt.executeQuery(query);
            
            // Weak MD5 hashing
            MessageDigest md = MessageDigest.getInstance("MD5");
            
            // Nested loops (performance issue)
            for (int i = 0; i < 10; i++) {
                for (int j = 0; j < 10; j++) {
                    for (int k = 0; k < 10; k++) {
                        System.out.println(i + ", " + j + ", " + k); // Excessive System.out.println
                    }
                }
            }
            
        } catch (Exception e) { // Catching base Exception
            // Empty catch block
        }
    }
    
    public void anotherMethod() {
        try {
            // Some code
        } catch (SQLException e) {
            // Empty catch block
        }
    }
}
