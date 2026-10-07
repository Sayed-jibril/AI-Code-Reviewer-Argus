// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BadContract {
    string private apiKey = "sk-1234567890abcdef"; // Hardcoded secret
    
    function badFunction(address user) public {
        // Security issues
        require(tx.origin == user, "Use msg.sender instead"); // tx.origin vulnerability
        
        // Low-level call (reentrancy risk)
        (bool success, ) = user.call{value: 1000}(""); // Dangerous low-level call
        
        // Selfdestruct dangerous
        selfdestruct(payable(user)); // Selfdestruct
        
        // Experimental pragma
        // pragma experimental ABIEncoderV2; // Experimental pragma
        
        // Unbounded loops can be gas-heavy
        for (uint i = 0; i < 1000; i++) {
            // Some operation
        }
    }
    
    function anotherFunction() public {
        // More issues
        require(msg.sender != address(0), "Invalid sender");
        revert("Error occurred");
        assert(msg.sender != address(0));
    }
}
