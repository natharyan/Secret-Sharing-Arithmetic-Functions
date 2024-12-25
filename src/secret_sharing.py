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
        if self.threshold > self.num_shares:
            raise ValueError("The pool secret will be irrecoverable, increase threshold")
        poly = [secret] + [self._RINT(self.prime-1) for i in range(self.threshold - 1)]
        points = [(i,self.eval_poly(poly,i,self.prime)) for i in range(1,self.num_shares + 1)]
        return points
    
    def recover_secret(self,shares):
        """
            Recover the secret from the shares
        """
        if len(shares) < self.threshold:
            raise ValueError(f"need at least {self.threshold} shares")
        x_s,y_s = zip(*shares)
        return utils._lagrange_interpolation(self.threshold,0,x_s,y_s,self.prime)
