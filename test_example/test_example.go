package main

import (
    "database/sql"
    "fmt"
    "math/rand"
    "os/exec"
    "unsafe"
)

var apiKey = "sk-1234567890abcdef" // Hardcoded secret

func badFunction(userInput string) {
    // Security issues
    query := "SELECT * FROM users WHERE id = " + userInput // SQL injection
    db.Query(query)
    
    cmd := exec.Command("ls", "-la", userInput) // Command injection risk
    cmd.Run()
    
    var ptr unsafe.Pointer // Unsafe pointer
    
    // Performance issues
    for i := 0; i < 10; i++ {
        for j := 0; j < 10; j++ {
            for k := 0; k < 10; k++ {
                fmt.Printf("%d, %d, %d\n", i, j, k)
            }
        }
    }
    
    // Memory issues
    slice := make([]int, 0)
    slice = append(slice, 1, 2, 3) // Slice append without capacity
    
    channel := make(chan int) // Channel without proper management
    
    // Quality issues
    _ = fmt.Sprintf("error") // Error ignored
    
    magicNumber := 12345 // Magic number
    
    defer fmt.Println("cleanup") // Defer usage
    
    // Go-specific patterns
    if err != nil {
        panic("error") // Panic in production
    }
}

func main() {
    badFunction("test")
}
