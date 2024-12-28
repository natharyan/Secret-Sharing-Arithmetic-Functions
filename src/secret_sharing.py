import random
import functools
import utils

class Shamir:
    def __init__(self,num_shares,threshold,prime_q=127):
        self.prime = 2**prime_q - 1
        self._RINT = functools.partial(random.SystemRandom().randint, 0)
        self.num_shares = num_shares
        self.threshold = threshold # minimum number of people required to recover the secret
    
    def eval_poly(self,poly,x,prime):
        """
            Evaluates the polynomial at x modulo prime
        """
        accum = 0
        for coeff in reversed(poly):
            accum = (accum * x + coeff) % prime
        return accum

    def split_secret(self,secret):
        """
            Split the secret into shares
        """
        # print("\nprime:",self.prime)
        if self.threshold > self.num_shares:
            raise ValueError("The pool secret will be irrecoverable, increase threshold")
        poly = [secret] + [self._RINT(self.prime-1) for i in range(self.threshold - 1)]
        print("\npolynomial of degree threshold-1 generated:")
        for i in range(len(poly)-1,-1,-1):
            print(str(poly[i]%self.prime) + 'x^' + str(i),end=" ")
        print()
        points = [(i,self.eval_poly(poly,i,self.prime)) for i in range(1,self.num_shares + 1)]
        return points
    
    def recover_secret(self,shares,threshold):
        """
            Recover the secret from the shares
        """
        if len(shares) < threshold:
            raise ValueError(f"need at least {threshold} shares")
        x_s,y_s = zip(*shares)
        utils._lagrange_interpolation(threshold,x_s,y_s,self.prime)
        return utils._lagrange_interpolation_evaluate_at_x(threshold,0,x_s,y_s,self.prime)
    
    def show_polynomial(self,shares):
        """
            Show the polynomial from the shares
        """
        x_s,y_s = zip(*shares)
        utils._lagrange_interpolation(self.threshold,x_s,y_s,self.prime)

class Operations:
    def add_shares(self,shares1,shares2,prime):
        """
            Add two shares from two polynomials and get the shares of the sum
        """
        shares = []
        for i in range(min(len(shares1),len(shares2))):
            shares.append((shares1[i][0],(shares1[i][1] + shares2[i][1]) % prime))
        return shares
    
    def add_public(self,shares,public_value,prime):
        """
            Add a public value to the shares
        """
        return [(share[0],share[1] + public_value % prime) for share in shares]
    
    def multiply_public(self,shares,public_value,prime):
        """
            Multiply a public value with the shares
        """

        return [(share[0],share[1] * public_value % prime) for share in shares]
    
    def beaver_triple(self,shares1,shares2,shamir):
        """
            Multiply two sets of shares using beaver triple without revealing x and y
        """
        _RINT_exc_0 = functools.partial(random.SystemRandom().randint, 1)
        a = _RINT_exc_0(shamir.prime-1)
        b = _RINT_exc_0(shamir.prime-1)
        c = (a*b) % shamir.prime
        x_a = (shamir.recover_secret(shares1,shamir.threshold) + a) % shamir.prime
        y_b = (shamir.recover_secret(shares2,shamir.threshold) + b) % shamir.prime
        shares_a = shamir.split_secret(a)
        shares_b = shamir.split_secret(b)
        shares_ab = shamir.split_secret(c)
        operations = Operations()
        neg_x_a_b_shares = operations.multiply_public(shares_b,-x_a,shamir.prime)
        neg_y_b_a_shares = operations.multiply_public(shares_a,-y_b,shamir.prime)
        add_shares = operations.add_shares(neg_x_a_b_shares,neg_y_b_a_shares,shamir.prime)
        add_shares_ab = operations.add_shares(add_shares,shares_ab,shamir.prime)
        add_public = operations.add_public(add_shares_ab,x_a*y_b,shamir.prime)
        return add_public
