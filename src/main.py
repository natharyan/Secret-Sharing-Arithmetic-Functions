from secret_sharing import Operations, Shamir
from exp import expression
from utils import prime
import getpass

operations = Operations()

def evaluate_expression_with_shares(x_shares, y_shares):
    """
    Evaluate the imported expression using secret shares.
    This function directly computes the expression result using the shares.
    """
    # Expression: 5 * (x ** 4) * y + 6 * x - 2 * y + x * y
    
    # x^4
    x_power_4 = x_shares
    for i in range(3):  # x^4 = x * x * x * x
        x_power_4 = operations.beaver_triple(x_power_4, x_shares, min(len(sharesx),len(sharesy)), max(thresholdx,thresholdy))
    
    # 5 * (x^4)
    term1_part = operations.multiply_public(x_power_4, 5, prime)
    
    # 5 * (x^4) * y
    term1 = operations.beaver_triple(term1_part, y_shares, min(len(sharesx),len(sharesy)), max(thresholdx,thresholdy))
    
    # 6 * x
    term2 = operations.multiply_public(x_shares, 6, prime)
    
    # -2 * y
    term3 = operations.multiply_public(y_shares, -2, prime)
    
    # x * y
    term4 = operations.beaver_triple(x_shares, y_shares, min(len(sharesx),len(sharesy)), max(thresholdx,thresholdy))
    
    # Add all terms: term1 + term2 + term3 + term4
    result = operations.add_shares(term1, term2, prime)
    result = operations.add_shares(result, term3, prime)
    result = operations.add_shares(result, term4, prime)
    
    return result

print("----------------- Secret Sharing with Arbitrary Numeric Functions -----------------")
secretx = int(getpass.getpass("Enter Secret x: "))
print(f"Secret x entered: {secretx}")
thresholdx = input("Enter Threshold for Retrieving x: ")
thresholdx = int(thresholdx)
num_sharesx = input("Enter Number of Shares for x (press Enter for default): ")
if not num_sharesx:
    num_sharesx = thresholdx + 5
else:
    num_sharesx = int(num_sharesx)

secrety = int(getpass.getpass("Enter Secret y: "))
print(f"Secret y entered: {secrety}")
thresholdy = input("Enter Threshold for Retrieving y: ")
thresholdy = int(thresholdy)
num_sharesy = input("Enter Number of Shares for y (press Enter for default): ")
if not num_sharesy:
    num_sharesy = thresholdy + 5
else:
    num_sharesy = int(num_sharesy)

max_threshold = max(thresholdx, thresholdy)
if num_sharesx < max_threshold:
    print(f"Warning: Number of shares for x ({num_sharesx}) is less than max threshold ({max_threshold}).")
    print("Adjusting number of shares for x to match the maximum threshold.")
    num_sharesx = max_threshold
if num_sharesy < max_threshold:
    print(f"Warning: Number of shares for y ({num_sharesy}) is less than max threshold ({max_threshold}).")
    print("Adjusting number of shares for y to match the maximum threshold.")
    num_sharesy = max_threshold

shamirx = Shamir(num_shares=num_sharesx,threshold=thresholdx)
sharesx = shamirx.split_secret(secretx)
shamiry = Shamir(num_shares=num_sharesy,threshold=thresholdy)
sharesy = shamiry.split_secret(secrety)
print(f"Created {len(sharesx)} shares for x and {len(sharesy)} shares for y")
if min(len(sharesx),len(sharesy)) < max(thresholdx,thresholdy):
    raise ValueError("The Minimum Number of Shares Should be Greater than the Maximum Threshold")

print(f"Evaluating expression 5 * (x ** 4) * y + 6 * x - 2 * y + x * y with secret shares...")
result = evaluate_expression_with_shares(sharesx, sharesy)

print("-> Result Shares: ",result)

shamir_result = Shamir(num_shares=min(num_sharesx,num_sharesy),threshold=max(thresholdx,thresholdy))
computed_secret = shamir_result.recover_secret(result,max(thresholdx,thresholdy))
poly = shamir_result.show_polynomial(result)
print()
print("-> Polynomial retrieved from the shares f(z) =",poly)
print("-> Computed Secret f(0) =",computed_secret)
expected_value = expression(secretx, secrety)
print("Expected Value =", expected_value)