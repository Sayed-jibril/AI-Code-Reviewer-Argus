fn main() {
    let api_key = "sk-1234567890abcdef"; // Hardcoded secret
    
    bad_function();
}

fn bad_function() {
    // Security issues
    unsafe {
        let ptr = std::ptr::null_mut();
        // Unsafe block
    }
    
    // Memory issues
    let vec = Vec::new(); // Vec without capacity
    let string = String::new(); // String without capacity
    
    let data = vec![1, 2, 3];
    let cloned = data.clone(); // Unnecessary clone
    
    let mut borrowed = &mut data; // Mutable borrow
    
    // Performance issues
    for i in 0..10 {
        for j in 0..10 {
            for k in 0..10 {
                println!("{}, {}, {}", i, j, k);
            }
        }
    }
    
    // Quality issues
    let magic_number = 12345; // Magic number
    
    let result = Some(42);
    let value = result.unwrap(); // unwrap() can panic
    
    let another_result = Some(42);
    let another_value = another_result.expect("should be 42"); // expect() can panic
    
    // Rust-specific patterns
    match value {
        42 => println!("forty two"),
        // Missing default case
    }
    
    enum BadEnum {
        Variant1,
        Variant2,
    }
    
    trait BadTrait {
        fn method(&self);
    }
    
    impl BadTrait for BadEnum {
        fn method(&self) {
            // Implementation
        }
    }
    
    macro_rules! bad_macro {
        ($x:expr) => {
            println!("{}", $x);
        };
    }
}
