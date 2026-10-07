<?php

$api_key = "sk-1234567890abcdef"; // Hardcoded secret

function bad_function($user_input) {
    // Security issues
    $query = "SELECT * FROM users WHERE id = " . $user_input; // SQL injection
    mysql_query($query);
    
    echo $user_input; // XSS risk
    
    eval("echo 'hello';"); // Dangerous eval
    
    exec("ls -la " . $user_input); // Command injection
    shell_exec("cat " . $user_input); // Command injection
    system("rm " . $user_input); // Command injection
    
    $hash = md5("password"); // Weak MD5
    $hash2 = sha1("password"); // Weak SHA1
    
    // Performance issues
    for ($i = 0; $i < 10; $i++) {
        for ($j = 0; $j < 10; $j++) {
            for ($k = 0; $k < 10; $k++) {
                echo "$i, $j, $k\n";
            }
        }
    }
    
    // Quality issues
    @mysql_connect(); // Error suppression
    
    try {
        // Some code
    } catch (Exception $e) {
        // Empty catch block
    }
    
    $magic_number = 12345; // Magic number
    
    $GLOBALS['var'] = 'value'; // Global variable
    
    $_GET['param']; // Direct superglobal access
    $_POST['param']; // Direct superglobal access
    
    // PHP-specific patterns
    include $user_input . '.php'; // Dynamic include
    require $user_input . '.php'; // Dynamic require
    
    unset($var); // Unset usage
    
    // Old style MySQL
    mysql_connect();
    mysql_select_db();
}

// Short tags
// <?= $variable ?>
