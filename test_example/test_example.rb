# Ruby test file with various issues

api_key = "sk-1234567890abcdef" # Hardcoded secret

def bad_function(user_input)
  # Security issues
  eval("puts 'hello'") # Dangerous eval
  
  system("ls -la #{user_input}") # Command injection
  exec("cat #{user_input}") # Command injection
  
  result = `ls #{user_input}` # Backticks can execute shell commands
  
  query = "SELECT * FROM users WHERE id = #{user_input}" # SQL injection
  
  hash = Digest::MD5.hexdigest("password") # Weak MD5
  
  # XSS risk
  puts "<%= #{user_input} %>"
  
  # Mass assignment
  user = User.new(params[:user])
  
  # Performance issues
  (0..9).each do |i|
    (0..9).each do |j|
      (0..9).each do |k|
        puts "#{i}, #{j}, #{k}"
      end
    end
  end
  
  # N+1 query pattern
  users.each do |user|
    user.posts.count # N+1 query
  end
  
  # Quality issues
  begin
    # Some code
  rescue => e
    # Empty rescue block
  end
  
  magic_number = 12345 # Magic number
  
  $global_var = "value" # Global variable
  
  @instance_var = "value" # Instance variable outside class
  
  puts "debug info" # puts in production code
  print "more debug" # print in production code
  
  # Ruby-specific patterns
  :symbol # Symbol usage
  
  users.each do |user|
    # Block parameter
  end
  
  def method_name
    # Method definition
  end
  
  class BadClass
    # Class definition
  end
  
  module BadModule
    # Module definition
  end
  
  attr_accessor :name # Attribute accessor
  
  require 'some_gem' # Require statement
  
  include SomeModule # Include statement
end

# Call the function
bad_function("test")
