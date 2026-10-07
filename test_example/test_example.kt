// Kotlin test file with various issues
package com.example

import java.sql.*

class BadService {
    
    private val apiKey = "sk-1234567890abcdef" // Hardcoded secret
    
    fun badFunction(userInput: String) {
        // Security issues
        val query = "SELECT * FROM users WHERE id = $userInput" // SQL concatenation
        val url = "http://insecure.com" // Insecure HTTP
        
        // Global mutable state
        var globalVar = "bad practice"
        
        // Performance issues
        for (i in 0..9) {
            for (j in 0..9) {
                for (k in 0..9) {
                    println("$i, $j, $k")
                }
            }
        }
        
        // Quality issues
        try {
            // Some operation
        } catch (e: Exception) { // Catching base Exception
            // Handle exception
        }
    }
    
    fun anotherFunction() {
        // MD5 usage
        val md = MessageDigest.getInstance("MD5")
        val hash = md.digest("password".toByteArray())
    }
}
