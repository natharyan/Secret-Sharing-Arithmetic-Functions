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

def _lagrange_interpolation_evaluate_at_x(threshold,x_eval,x_s,y_s,prime):
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

def _polynomial_multiply(poly1, poly2, prime):
    """
        Multiply two polynomials with coefficients in modulo prime
    """
    result = [0] * (len(poly1) + len(poly2) - 1)
    for i in range(len(poly1)):
        for j in range(len(poly2)):
            result[i + j] = (result[i + j] + poly1[i] * poly2[j]) % prime
    return result

def _lagrange_interpolation(threshold, x_s, y_s, prime):
    """
        Generates the polynomial with x_s and y_s, with coefficients in modulo prime
    """
    result = [0] * threshold
    for i in range(threshold):
        denoms = [(x_s[i] - x_s[j]) % prime for j in range(threshold) if j != i]
        denom_product = functools.reduce(lambda x, y: (x * y) % prime, denoms)
        current_poly = [1]
        for j in range(threshold):
            if j != i:
                term = [(-x_s[j]) % prime, 1]
                current_poly = _polynomial_multiply(current_poly, term, prime)
        scale_factor = _divmod(y_s[i], denom_product, prime)
        current_poly = [(coeff * scale_factor) % prime for coeff in current_poly]
        for j in range(len(current_poly)):
            result[j] = (result[j] + current_poly[j]) % prime
    # print("\nretrieved polynomial:")
    coeffs = []
    for i in range(len(result)-1, -1, -1):
        if result[i] != 0:
            coeffs.append(f"{result[i]}z^{i}")
    # print(" ".join(coeffs))
    polynomial = " + ".join(coeffs)
    return polynomial