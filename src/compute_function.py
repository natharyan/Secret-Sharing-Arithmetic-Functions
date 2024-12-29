from secret_sharing import Operations, Shamir

operators = ['+','-','*','^']
secretvars = ['x','y']
parenthesis = ['(',')']

operations = Operations()

q = 127
prime = 2**q - 1

# TODO: take as user inputs along with secrets
thresholdx = 5
thresholdy = 6


sharesx = [1,2,3]
sharesy = [4,5,6]
shares_dict = {'x':sharesx,'y':sharesy}

class Node:
    def __init__(self, value, operator=False,secret=False):
        self.value = value # operator, number(int), shares(list)
        self.operator = operator
        self.secret = False
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
    expression = expression.replace(" ","")
    tokens = list(expression)
    i = 0
    while i < len(tokens):
        if i!=len(tokens)-1 and tokens[i] not in operators+['('] and tokens[i+1] not in operators+[')']:
            tokens.insert(i+1,'*')
        i += 1
    print("Infix:",tokens)
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
                print("right:",right)
            if left in secretvars:
                left = shares_dict[left]
                print("left:",left)
            
            operator_parent = Node(postfix[i],operator=True,secret=False)
            operator_parent.left = left
            operator_parent.right = right
            stack.append(operator_parent)
    root = stack.pop()
    return root


expression = input("Expression: ")
root = build_parsetree(expression)

print(root.value,root.left.value,root.right.value)

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
    
    if not node.operator:
        return node.value
    else:
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
            if not isinstance(node.right.value,int):
                ValueError(f"cannot parse {node.left.value}^{node.right.value}")
            elif isinstance(left,list):
                expval_shar = left
                for i in range(node.right.value-1):
                    expval_shar = operations.beaver_triple(expval_shar,left,min(len(sharesx),len(sharesy)),max(thresholdx,thresholdy))
            elif isinstance(left,int):
                expval = left
                for i in range(node.right.val - 1):
                    expval = expval*left
        