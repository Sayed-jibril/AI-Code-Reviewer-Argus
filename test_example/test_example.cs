using System;
using System.Data.SqlClient;
using System.Security.Cryptography;
using System.Threading.Tasks; // Added missing import for Task.Delay

public class BadClass
{
    private string ApiKey = "sk-1234567890abcdef"; // Hardcoded secret
    
    public void BadMethod(string userInput)
    {
        try
        {
            // SQL concatenation (injection risk)
            string query = "SELECT * FROM users WHERE id = " + userInput;
            SqlCommand cmd = new SqlCommand(query);
            
            // Weak MD5 hashing
            MD5 md5 = MD5.Create();
            
            // Non-cryptographic random
            Random rng = new Random();
            
            // Nested loops (performance issue)
            for (int i = 0; i < 10; i++)
            {
                for (int j = 0; j < 10; j++)
                {
                    for (int k = 0; k < 10; k++)
                    {
                        Console.WriteLine($"{i}, {j}, {k}");
                    }
                }
            }
            
            // SqlConnection without using statement
            SqlConnection conn = new SqlConnection("connection_string");
            
        }
        catch (Exception ex) // Catching base Exception
        {
            // Empty catch block
        }
    }
    
    // Async void (avoid except for event handlers)
    public async void BadAsyncMethod()
    {
        await Task.Delay(1000);
    }
}
