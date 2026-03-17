"""
Module for tokenizing, parsing, and evaluating expressions.
"""


class EmptyStructureError(Exception):
    """
    Raised when stack or queue is empty and illegal operation is performed.
    """
    def __init__(self):
        super().__init__("Structure may not be empty when peeking or popping!")


class UnknownCharError(Exception):
    """
    Raised when illegal character is present in expression.
    """
    def __init__(self, expression: str):
        """
        :param expression: The expression with an unknown character.
        """
        super().__init__(f"Unknown character: {expression}")


class MissingOperatorError(Exception):
    """
    For when an expression is missing operators. This should not be called when the expression has just one number.
    """
    def __init__(self):
        super().__init__("Missing operator in expression!")


class Node:
    """
    Node in a singly linked list (used in implementation of stack and queue)
    """
    def __init__(self, value: float | str):

        self.value = value
        self.next = None


class Stack:
    """
    Implementation of a stack using a linked list
    """

    def __init__(self, top: Node = None):
        """
        :param top: The top node. None by default.
        """

        self.top = top

    def __str__(self):
        """
        Returns string representation of content of stack. This should only be used for debugging as traversing the stack violates LIFO.

        :return: String representation of stack contents
        """

        result = ""

        current_node = self.top
        while current_node is not None:
            result += str(current_node.value) + " "
            current_node = current_node.next

        return result

    def push(self, value: float | str):
        """
        Push element onto the stack

        :param value: The value to push on the stack
        :return:
        """

        new_node = Node(value)
        new_node.next = self.top
        self.top = new_node

    def pop(self) -> float | str:
        """
        Pop element from top of stack. The stack may not be empty.

        :return: The value stored in the top node.
        """

        if self.is_empty():
            raise EmptyStructureError()

        value = self.top.value
        self.top = self.top.next
        return value

    def peek(self) -> float | str:
        """
        Peek the top of the stack. The stack may not be empty.

        :return: The value stored in the top node.
        """

        if self.is_empty():
            raise EmptyStructureError()

        return self.top.value

    def is_empty(self) -> bool:
        """
        Check whether the stack is empty.

        :return: Returns True if empty, False otherwise
        """

        return self.top is None


class ExpressionStack(Stack):

    def __init__(self, top: Node = None):
        """
        Inherits from Stack, but has methods defined to run calculations on the numbers inside of it.

        :param top: The top of the stack. None by default.
        """
        super().__init__(top)

        self.operator_functions = {
            "+": self.add,
            "-": self.subtract,
            "*": self.multiply,
            "/": self.divide,
            "~": self.negate,
            "^": self.power
        }

    def add(self):
        """
        Add the top two members of the stack and push the result to the stack.
        :return:
        """
        b = self.pop()
        a = self.pop()
        self.push(a + b)

    def subtract(self):
        """
        Subtract the top two members of the stack and push the result to the stack
        :return:
        """
        b = self.pop()
        a = self.pop()
        self.push(a - b)

    def multiply(self):
        """
        Multiply the top two members of the stack and push the result to the stack.
        :return:
        """
        b = self.pop()
        a = self.pop()
        self.push(a * b)

    def divide(self):
        """
        Divide the top two members of the stack and push the result to the stack.
        :return:
        """
        b = self.pop()
        a = self.pop()
        self.push(a / b)

    def negate(self):
        """
        Negate the top member of the stack and push the result to the stack.
        :return:
        """
        a = self.pop()
        self.push(-a)

    def power(self):
        """
        Raise the second-highest member of the stack to the highest member of the stack and push the result to the stack.
        :return:
        """
        b = self.pop()
        a = self.pop()
        self.push(a ** b)

    @property
    def result(self):
        """
        :return: Returns the top member of the stack.
        """
        return self.pop()


class Queue:
    """
    Implementation of a queue using a linked list
    """
    def __init__(self, front: Node = None):
        """
        :param front: The front of the queue. None by default.
        """

        self.front = front
        self.tail = self.front

    def __str__(self):
        """
        Returns string representation of content of queue. This should only be used for debugging as traversing the queue violates FIFO.

        :return: String representation of queue contents
        """

        result = ""

        current_node = self.front
        while current_node is not None:
            result += str(current_node.value) + " "
            current_node = current_node.next

        return result

    def enqueue(self, value: float | str):
        """
        Enqueue an element into the queue

        :param value: The value to enqueue
        :return:
        """

        if self.is_empty():
            self.front = Node(value)
            self.tail = self.front

        else:
            new_node = Node(value)
            self.tail.next = new_node
            self.tail = new_node

    def dequeue(self) -> float | str:
        """
        Dequeue element from front of queue. The queue may not be empty.

        :return: The value stored in the front node.
        """

        if self.is_empty():
            raise EmptyStructureError()

        value = self.front.value
        self.front = self.front.next
        return value

    def peek(self) -> float | str:
        """
        Peek element at front of queue. The queue may not be empty.

        :return: The value stored in the front node.
        """

        if self.is_empty():
            raise EmptyStructureError()

        return self.front.value

    def is_empty(self) -> bool:
        """
        Check whether the queue is empty.

        :return: Returns True if empty, False otherwise
        """

        return self.front is None


def tokenize(expression: str):
    """
    Tokenize string containing a mathematical expression. This assumes the string is a well-formed expression.

    :param expression: String representing the arithmetic expression to be tokenized in infix notation
    :return: List holding tokenized expression
    """

    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
    operators = ["-", "+", "/", "*", "^", "(", ")"]  # these precede negation except for ")"

    tokens = []

    # Remove spaces
    despaced_expression = expression.replace(" ", "")

    # This will hold a partial number while we tokenize the expression
    number_buffer = ""

    # Run through expression finding tokens, replacing negation with ~
    for index in range(len(despaced_expression)):
        symbol = despaced_expression[index]

        # if we're at the beginning of the expression or the preceding symbol is an operator (but not closing parenthesis) then it might be negation
        # specifically it's negation if the symbol is - which we check later
        preceding_symbol = despaced_expression[index - 1]
        negation_possible = (index == 0 or (preceding_symbol in operators and preceding_symbol != ")"))

        if symbol in digits:
            number_buffer += symbol
        elif symbol in operators:
            # if the number buffer isn't empty, and we hit an operator, tokenize what's in it and clear the buffer
            if len(number_buffer) > 0:
                # make sure it doesn't start or end in . because that makes bad things happen
                if number_buffer[-1] == "." or number_buffer[0] == ".":
                    raise ValueError
                tokens.append(float(number_buffer))
                number_buffer = ""
            # if we see a minus sign and the conditions in negation_possible are true, it's negation
            if symbol == "-" and negation_possible:
                # Replace negation symbol with ~ so parsing later is clear on what it represents
                tokens.append("~")
            else:
                tokens.append(symbol)
        else:
            # not a digit or operator, there's something else in this expression we can't read
            raise UnknownCharError(expression)

    # Make sure we didn't leave anything in the number buffer
    if len(number_buffer) > 0:
        if number_buffer[-1] == "." or number_buffer[0] == ".":
            # make sure it doesn't start or end in . because that makes bad things happen
            raise ValueError
        tokens.append(float(number_buffer))

    return tokens


def parse(infix_expression: list):
    """
    Parse an infix expression into postfix notation using the shunting yard algorithm.

    :param infix_expression: List representing the tokenized arithmetic expression to be parsed in infix notation
    :return: Queue holding expression in postfix notation
    """

    # order of operations and associativity (left associative or right associative)
    operator_information = {
        "-": (0, "L"),
        "+": (0, "L"),
        "/": (1, "L"),
        "*": (1, "L"),
        "~": (2, "R"),
        "^": (3, "R")
    }

    # if there are no operators in our infix expression (disjoint with the set of operators) and there is more than one number in the expression, we have a malformed expression
    if set(operator_information.keys()).isdisjoint(infix_expression) and sum(isinstance(i, float) for i in infix_expression) > 1:
        raise MissingOperatorError()

    # stack holding operators and output queue
    operator_stack = Stack()
    output_queue = Queue()

    for token in infix_expression:
        if isinstance(token, float):
            output_queue.enqueue(token)
        elif token == "(":
            # this token will mark where we stop popping when we find a closing parenthesis
            operator_stack.push(token)
        elif token == ")":
            # pop all operators until we find the matching open parenthesis
            while operator_stack.peek() != "(":
                output_queue.enqueue(operator_stack.pop())
            # remove open parenthesis
            operator_stack.pop()
        else:
            # ok so it must be an operator
            # if the current top operator has greater precedence than the one we're on, that has to be taken care of

            # conditions: stack isn't empty, peek is a valid operator (in info dict), if left associative >=, if right associative >
            while not operator_stack.is_empty() and operator_stack.peek() in operator_information and ((operator_information[operator_stack.peek()][0] >= operator_information[token][0] and operator_information[token][1] == "L") or (operator_information[operator_stack.peek()][0] > operator_information[token][0] and operator_information[token][1] == "R")):
                output_queue.enqueue(operator_stack.pop())

            # now we can push the operator to the stack
            operator_stack.push(token)

    while not operator_stack.is_empty():
        output_queue.enqueue(operator_stack.pop())

    return output_queue


def calculate(postfix_expression: Queue):
    """
    Calculate value of expression using stack-based calculator

    :param postfix_expression: Queue holding expression in postfix notation
    :return: Value of expression
    """

    expression_stack = ExpressionStack()

    current_node = postfix_expression.front

    while current_node is not None:
        if isinstance(current_node.value, float):
            expression_stack.push(current_node.value)
        else:
            expression_stack.operator_functions[current_node.value]()
        current_node = current_node.next
    return expression_stack.result


def evaluate(expression: str):
    """
    Tokenize, parse, and calculate mathematical expression, removing decimal part if possible.
    :param expression: The expression to evaluate
    :return: Evaluation of expression
    """

    # for easy exception handling we can just use a dict (time complexity O(1)!!! wow!!!)
    exception_dict = {
        OverflowError: "Overflow",
        UnknownCharError: "Foreign Character",
        EmptyStructureError: "Malformed Expression",
        KeyError: "Malformed Expression",
        ValueError: "Malformed Expression",
        MissingOperatorError: "Missing Operator"
    }

    try:
        value = calculate(parse(tokenize(expression)))

    except tuple(exception_dict.keys()) as exception:
        return exception_dict[type(exception)]

    # unknown error we were not able to catch
    except Exception as exception:
        print(exception)
        return "Unknown Error (See Console)"

    # if we have a float divisible by 1 (so a whole number, cast to an int to get rid of the .0)
    if isinstance(value, float) and value % 1 == 0:
        value = int(value)

    return value


if __name__ == "__main__":
    # this is really gross
    assert (evaluate("") == "Malformed Expression")  # empty structure error
    assert (evaluate("3++2") == "Malformed Expression")  # also empty structure error
    assert (evaluate("3+((2)-5") == "Malformed Expression")  # key error
    assert (evaluate("5i+2i") == "Foreign Character")  # unknown character error
    assert (evaluate("5.. + 2.2") == "Malformed Expression")  # value error
    assert (evaluate("0.(3)") == "Malformed Expression")  # another value error
    assert (evaluate("(4).5") == "Malformed Expression")  # another one
    assert (evaluate("9(3)") == "Missing Operator")  # missing operator
    assert (evaluate("(92)3") == "Missing Operator")  # missing operator
    assert (abs(evaluate("2 + 3") - 5) < 1e-9)
    assert (abs(evaluate("10 - 7") - 3) < 1e-9)
    assert (abs(evaluate("2 + 3 * 4") - 14) < 1e-9)
    assert (abs(evaluate("(2 + 3) * 4") - 20) < 1e-9)
    assert (abs(evaluate("2^3") - 8) < 1e-9)
    assert (abs(evaluate("3 + 4 * 2 / (1 - 5)^2") - 3.5) < 1e-9)
    assert (abs(evaluate("5 + ((1 + 2) * 4) - 3") - 14) < 1e-9)
    assert (abs(evaluate("4 + -2") - 2) < 1e-9)
    assert (abs(evaluate("-2 * -3") - 6) < 1e-9)
    assert (abs(evaluate("3.5 + 2.1") - 5.6) < 1e-9)
    assert (abs(evaluate("2.5 * 4") - 10) < 1e-9)
    assert (abs(evaluate("2 + 3 * 4 - 5 / 2") - 11.5) < 1e-9)
    assert (abs(evaluate("2^3^2") - 512) < 1e-9)
    assert (abs(evaluate("-(3 + 2)") - (-5)) < 1e-9)
    assert (abs(evaluate("0^0") - 1) < 1e-9)
    assert (abs(evaluate("3 + 4 * 2 / (1 - 5)^2^2") - 3.03125) < 1e-9)
