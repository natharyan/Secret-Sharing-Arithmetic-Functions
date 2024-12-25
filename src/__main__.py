from secret_sharing import Shamir
import random

if __name__ == "__main__":
    secret = 5604
    num_shares = int(input("enter number of shares: "))
    threshold = input("enter threshold (enter for def): ")
    if not threshold:
        threshold = 2
    else:
        threshold = int(threshold)
    shamir = Shamir(num_shares=num_shares,threshold=threshold)
    shares = shamir.split_secret(secret)
    # print(f"shares: {shares}")
    # randomly select threshold number of shares
    shares_come_together = random.sample(shares,threshold)
    print(f"recovered Secret: {shamir.recover_secret(shares_come_together)}")