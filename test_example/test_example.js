// JavaScript test file with various issues
const apiKey = "sk-1234567890abcdef"; // Hardcoded secret

function badFunction(items = []) { // Mutable default
    var unusedVar = "never used"; // Using var instead of let/const
    
    try {
        const result = items[0];
        eval("console.log(result)"); // Dangerous eval usage
        document.write("<script>alert('xss')</script>"); // Unsafe document.write
        element.innerHTML = userInput; // XSS risk
        location.href = userInput; // Unvalidated redirect
    } catch (e) { // Broad catch
        // Empty catch block
    }
    
    // Nested loops (performance issue)
    for (let i = 0; i < 10; i++) {
        for (let j = 0; j < 10; j++) {
            for (let k = 0; k < 10; k++) {
                document.querySelector('.item'); // DOM query in loop
            }
        }
    }
    
    // Weak equality
    if (result == "test") {
        console.log("weak equality");
    }
    
    return result;
}

// Arrow function
const arrowFunc = () => {
    const hash = md5("password"); // Weak MD5 hashing
    return hash;
};
