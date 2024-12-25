import functools

def _extended_gcd(a,b):
    """
        Extended Euclidean Algorithm for finding the GCD of two numbers.
        inv, g such that a*inv + b*m = 1
        returns (inv,m)
    """
    x,y, u,v = 0,1, 1,0

    while b!=0:
        q = a//b
        a,b = b,a%b
        x,u = u - q*x,x
        y,v = v - q*y,y
    
    return u,v

def _divmod(num,denom,prime):
    """
        Return num/den module modulo prime
        which is equivalent to num * inv(den) mod prime
    """
    inv,_ = _extended_gcd(denom,prime)
    inv = inv % prime
    return (num * inv) % prime

def _lagrange_interpolation(threshold,x_eval,x_s,y_s,prime):
    """
        Given threshold number of points, and (x,y) coordinates stored in x_s and y_s
        respectively, this function uses Lagrange interpolation to find the value of the polynomial
        at x_eval
    """
    lagrange_basis_polynomials = []
    for i in range(threshold):
        nums = [(x_eval - x_s[k]) for k in range(threshold) if k!=i]
        denoms = [(x_s[i] - x_s[k]) for k in range(threshold) if k!=i]
        prod_nums = functools.reduce(lambda x,y: x*y, nums)
        prod_denoms = functools.reduce(lambda x,y: x*y, denoms)
        lagrange_basis_polynomials.append(_divmod(prod_nums,prod_denoms,prime))
    f_at_x_eval = 0
    for i in range(len(lagrange_basis_polynomials)):
        f_at_x_eval += y_s[i]*lagrange_basis_polynomials[i]
    return f_at_x_eval % prime