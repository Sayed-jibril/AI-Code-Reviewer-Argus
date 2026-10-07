import os
import json
import pickle
import hashlib
from typing import List, Dict

# Unused import
import sys

# Hardcoded secret (will be detected)
api_key = "sk-1234567890abcdef"

def bad_function(items=[], config={}):  # Mutable defaults
    """Function with mutable default arguments"""
    unused_var = "this is never used"
    
    try:
        result = items[0]
    except:  # Broad except
        result = None
    
    # Nested loops (performance issue)
    for i in range(10):
        for j in range(10):
            for k in range(10):
                print(i, j, k)
    
    # Dangerous eval usage
    eval("print('dangerous')")
    
    # Weak MD5 hashing
    hash_value = hashlib.md5(b"password").hexdigest()
    
    # Raw SQL (injection risk)
    query = "SELECT * FROM users WHERE id = " + str(result)
    
    return result

def load_data(data_string):
    """Function with unsafe pickle usage"""
    return pickle.loads(data_string)  # Security risk

# Unused variable
unused_global = "never referenced"
