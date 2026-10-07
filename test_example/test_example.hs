-- Haskell test file with various issues
module BadModule where

import System.IO.Unsafe (unsafePerformIO)
import Data.Maybe (fromJust)

-- Hardcoded secret
apiKey :: String
apiKey = "sk-1234567890abcdef"

-- unsafePerformIO can break purity/safety
badFunction :: IO String
badFunction = do
    let result = unsafePerformIO (return "dangerous")
    return result

-- Partial functions can crash on bad input
dangerousFunction :: [Int] -> Int
dangerousFunction xs = head xs + tail xs !! 0

-- Potential heavy recursion; check termination
recursiveFunction :: Int -> Int
recursiveFunction n = if n <= 0 then 1 else n * recursiveFunction (n - 1)

-- Another partial function
fromJustFunction :: Maybe Int -> Int
fromJustFunction mx = fromJust mx

-- Pattern matching
patternMatch :: Int -> String
patternMatch 0 = "zero"
patternMatch 1 = "one"
-- Missing default case

-- Let binding
letBinding :: Int -> Int
letBinding x = let y = x * 2
                   z = y + 1
               in z
