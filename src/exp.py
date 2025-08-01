from utils import prime

def expression(x, y):
    return (5 * (x ** 4) * y + 6 * x - 2 * y + x * y) % prime
