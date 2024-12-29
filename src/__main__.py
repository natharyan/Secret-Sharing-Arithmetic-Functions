from secret_sharing import Operations, Shamir

operators = ['+','-','*','^']
secretvars = ['x','y']
parenthesis = ['(',')']

operations = Operations()

q = 127
prime = 2**q - 1

thresholdx = 0
thresholdy = 0
sharesx = []
sharesy = []

shares_dict = {'x':sharesx,'y':sharesy}

class Node:
    def __init__(self, value):
        self.value = value # operator value
        self.left = None
        self.right = None

def shunting_yard_postfix(infix):
    precedence = {'+':1,'-':1,'*':2,'^':3}
    stack = []
    postfix = []
    for token in infix:
        if token in operators:
            while stack and precedence.get(stack[-1],0) >= precedence.get(token,0):
                postfix.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            stack.pop()
        else:
            postfix.append(token)
    while stack:
        if stack[-1] in ['(',')']:
            raise ValueError("mismatched parenthesis")
        postfix.append(stack.pop())
    return postfix

def build_parsetree(expression):
    print("thresholdx:",thresholdx)
    print("thresholdy:",thresholdy)
    expression = expression.replace(" ","")
    tokens = list(expression)
    i = 0
    while i < len(tokens):
        if i!=len(tokens)-1 and tokens[i] not in operators+['('] and tokens[i+1] not in operators+[')']:
            tokens.insert(i+1,'*')
        i += 1
    print("Infix:",tokens)
    if all(token not in operators for token in tokens):
        raise ValueError("no operators in the expression")
    postfix = shunting_yard_postfix(tokens)
    print("Postfix:",postfix)
    stack = []
    for i in range(len(postfix)):
        if postfix[i] not in operators:
            stack.append(postfix[i])
        else:
            right = stack.pop()
            left = stack.pop()

            if right in secretvars:
                right = shares_dict[right]
            if left in secretvars:
                left = shares_dict[left]
            if type(right) == str and str.isdigit(right):
                right = int(right)
            if type(left) == str and str.isdigit(left):
                left = int(left)
            # print((left,right))
            operator_parent = Node(postfix[i])
            operator_parent.left = left
            operator_parent.right = right
            stack.append(operator_parent)
    root = stack.pop()
    return root

def evaluate_tree(node):
    # base case
    if isinstance(node,int) or isinstance(node,list):
        return node
    
    left = evaluate_tree(node.left)
    right = evaluate_tree(node.right)

    left_eval_secret = isinstance(left,list) and isinstance(right,int)
    right_eval_secret = isinstance(left,int) and isinstance(right,list)
    both_eval_secret = isinstance(left,list) and isinstance(right,list)
    both_eval_public = isinstance(left,int) and isinstance(right,int)
    
    if node.value == "+":
        if left_eval_secret:
            return operations.add_public(left,right,prime)
        elif right_eval_secret:
            return operations.add_public(right,left,prime)
        elif both_eval_secret:
            return operations.add_shares(left,right,prime)
        elif both_eval_public:
            return left + right
    elif node.value == "-":
        if left_eval_secret:
            return operations.add_public(left,-right,prime)
        elif right_eval_secret:
            right = operations.multiply_public(right,-1,prime)
            return operations.add_public(right,left,prime)
        elif both_eval_secret:
            right = operations.multiply_public(right,-1,prime)
            return operations.add_shares(left,right,prime)
        elif both_eval_public:
            return left - right
    elif node.value == "*":
        if left_eval_secret:
            return operations.multiply_public(left,right,prime)
        elif right_eval_secret:
            return operations.multiply_public(right,left,prime)
        elif both_eval_secret:
            return operations.beaver_triple(left,right,min(len(sharesx),len(sharesy)),max(thresholdx,thresholdy))
        elif both_eval_public:
            return left*right
    # only for integral powers, can raise it to the power of a secret if there is a way to do so without revealing the secret itself
    elif node.value == "^":
        if not isinstance(right,int):
            ValueError(f"cannot parse {left}^{right}")
        elif isinstance(left,list):
            expval_shar = left
            for i in range(right-1):
                expval_shar = operations.beaver_triple(expval_shar,left,min(len(sharesx),len(sharesy)),max(thresholdx,thresholdy))
            return expval_shar
        elif isinstance(left,int):
            expval = left
            for i in range(right - 1):
                expval = expval*left
            return expval

print("----------------- Secret Sharing with Arbitrary Numeric Functions -----------------")
secretx = int(input("Enter Secret x: "))
thresholdx = input("Enter Threshold for Retrieving x (press Enter for default): ")
if not thresholdx:
    thresholdx = 2
else:
    thresholdx = int(thresholdx)
num_sharesx = input("Enter Number of Shares for x (press Enter for default): ")
if not num_sharesx:
    num_sharesx = 0
else:
    num_sharesx = int(num_sharesx)

secrety = int(input("Enter Secret y: "))
thresholdy = input("Enter Threshold for Retrieving y (press Enter for default): ")
if not thresholdy:
    thresholdy = 2
else:
    thresholdy = int(thresholdy)
num_sharesy = input("Enter Number of Shares for y (press Enter for default): ")
if not num_sharesy:
    num_sharesy = 0
else:
    num_sharesy = int(num_sharesy)

if num_sharesx == 0 or num_sharesy == 0:
    num_sharesx = num_sharesy = max(thresholdx,thresholdy) + 5

shamirx = Shamir(num_shares=num_sharesx,threshold=thresholdx)
sharesx = shamirx.split_secret(secretx)
shamiry = Shamir(num_shares=num_sharesy,threshold=thresholdy)
sharesy = shamiry.split_secret(secrety)
print(len(sharesx),len(sharesy))
if min(len(sharesx),len(sharesy)) < max(thresholdx,thresholdy):
    raise ValueError("The Minimum Number of Shares Should be Greater than the Maximum Threshold")

shares_dict['x'] = sharesx
shares_dict['y'] = sharesy

# Example expression: 5(x^4)y+6x-2y+xy
expression = input("Expression: ")
root = build_parsetree(expression)

result = evaluate_tree(root)

print("Result: ",result)

shamir_result = Shamir(num_shares=min(num_sharesx,num_sharesy),threshold=max(thresholdx,thresholdy))
computed_secret = shamir_result.recover_secret(result,max(thresholdx,thresholdy))

print("Computed Secret: ",computed_secret)