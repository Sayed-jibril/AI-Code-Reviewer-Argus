import Foundation

// Swift test file with various issues
let apiKey = "sk-1234567890abcdef" // Hardcoded secret

class BadViewController: UIViewController {
    
    func badFunction() {
        // Security issues
        let url = URL(string: "http://insecure.com")! // Insecure HTTP URL
        let hash = MD5("password") // Weak MD5
        
        // Force unwrapping
        let value = someOptional! // Force unwrap may crash
        
        // Force try
        try! someRiskyOperation() // Force try may crash
        
        // Performance issues
        for i in 0..<10 {
            for j in 0..<10 {
                for k in 0..<10 {
                    print("\(i), \(j), \(k)")
                }
            }
        }
        
        // Quality issues
        do {
            try someOperation()
        } catch {
            // Empty catch block
        }
    }
    
    func anotherFunction() {
        // NSExpression usage (eval-like)
        let expression = NSExpression(format: "1 + 2")
        let result = expression.expressionValue(with: nil, context: nil)
    }
}
