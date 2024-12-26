from secret_sharing import Shamir, Operations
import random

if __name__ == "__main__":
    print("\n-----------------secret sharing using Shamir's secret sharing scheme-----------------")
    secret = 5604
    num_shares = int(input("enter number of shares: "))
    threshold = input("enter threshold (enter for def): ")
    if not threshold:
        threshold = 2
    else:
        threshold = int(threshold)
    shamir = Shamir(num_shares=num_shares,threshold=threshold)
    shares = shamir.split_secret(secret)
    print(f"\nshares generated: \n{shares}")
    shares_come_together = random.sample(shares,threshold)
    # print("\nshares used for secret recovery:")
    # print(shares_come_together)

    print(f"\nrecovered secret: {shamir.recover_secret(shares_come_together,threshold)}")

    secret1 = 7706
    num_shares1 = int(input("\nenter number of shares: ")) 
    threshold1 = input("enter threshold (enter for def): ")
    if not threshold1:
        threshold1 = 2
    else:
        threshold1 = int(threshold1)
    shamir1 = Shamir(num_shares=num_shares1,threshold=threshold1)
    shares1 = shamir1.split_secret(secret1)
    print(f"\nshares generated: \n{shares1}")
    
    # while defining the number of shares, make sure that the number of shares in both the shamir objects are greater than the maximum threshold
    shamir2 = Shamir(num_shares=min(num_shares,num_shares1),threshold=max(threshold,threshold1))

    # add shares
    print("\n-----------------addition of shares-----------------")
    threshold_add = max(threshold,threshold1)
    print(f"\ngiven the polynomials:")
    shamir.show_polynomial(shares)
    shamir1.show_polynomial(shares1)
    print()
    operations = Operations()
    shares_added = operations.add_shares(shares,shares1,shamir2.prime)
    print("\nadded shares:")
    print(shares_added)
    # print("\nshares used for secret recovery:")
    # print(random.sample(shares_added,threshold_add))
    print(f"\nrecovered secret: {shamir2.recover_secret(shares_added,shamir2.threshold)}")

    # addition of shares with a public value
    print("\n-----------------addition of shares with public value-----------------")
    print("\nOriginal Polynomial:")
    shamir1.show_polynomial(shares1)
    public_value = 100
    shares_added_with_public = operations.add_public(shares1,public_value,shamir1.prime)
    print(f"\nPolynomial with added public value {public_value}:")
    print(f"\nRetrieved secret: {shamir1.recover_secret(shares_added_with_public,threshold1)}")
    
    print("\n-----------------multiplication of shares with public value-----------------")
    print("\nOriginal Polynomial:")
    shamir1.show_polynomial(shares1)
    public_value = 120
    shares_multiplied_with_public = operations.multiply_public(shares1,public_value,shamir1.prime)
    print(f"\nPolynomial with multiplied public value {public_value}:")
    print(f"\nRetrieved secret: {shamir1.recover_secret(shares_multiplied_with_public,threshold1)}")

    print("\n-----------------multiplication of two sets of shares-----------------")
    