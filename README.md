# The Funny Calc*
This is a very funny calc that was conceived by my friend Wyatt Ballweber that I built using Python's `tkinter` library. It has a "funny mode" that causes the calculator to always return a value very close to the correct answer but always wrong. Happy calculating!

**\*Calc** is short for calculator. I'm just using slang, chat.

## The Backend

This is the part of the README where I yap about what I did on the backend because I think it's pretty cool (if very basic in the grand scheme of things).

First, an **operator** is a symbol like +, -, or ^ that indicate a certain action to be performed on **operands**. Basic calculators like this one use **arithmetic operators** meaning they perform mathematical operations on numbers. They can be **unary**, meaning they act on one operand; **binary**, meaning they act on two operands, or have higher **arities**. In this calculator, we only work with unary and binary operators.

### Tokenization

The first step in evaluating an expression we get from the calculator app is **tokenizing** the input, or splitting it into individual **tokens**, smaller parts of our expression. For example, the expression `'5.2 + (2.1 * 3.9)'` would be tokenized as `[5.2, '+', '(', 2.1, '*', 3.9, ')']`. We run through each character in the expression and if it's an accepted operator, we add it to the list of tokens. If we see a number or decimal point (.), we add it to a **number buffer** (just a string) and the next time we see an operator (or at the end of our expression) we add what's in the number buffer to our list of tokens (converting it to a float).

We must also ensure that we can differentiate between **unary negation** (-x) and **binary subtraction** (a - b). Note that this is determined **only by what precedes the hyphen.** If it is another subexpression, we have subtraction, but if it is an operator or the beginning of our expression, it must be negation. So we check the preceding symbol and if it's the beginning of our expression or an operator (but **not** the closing parenthesis because that indicates another subexpression), we **replace it with a special symbol denoting negation (~).**

### Parsing

There are many different ways to read the same mathematical expression, and each has its own pros and cons. The notation you are likely most used to is **infix notation**, where the operators are on either side of the operand, as in expressions like `2 + (7 - 4) * (6 / 3)`. 

Another notation that we use in this calculator for reasons that will be explained in a moment is **postfix notation** (also known as **reverse Polish notation** after Jan Łukasiewicz), where the operators come after the operands. The expression above in postfix notation would be rendered as `2 7 4 - 6 3 / * +`. This means we reduce 7 by 4, then divide 6 by 3, multiply these two numbers and then add the result to 2.

Note a key advantage of postfix notation: the numbers are in the same order, but we don't need parentheses to show the order of operations! The order we run the operations is inherent in the notation. This makes it easier for a machine to process the expression because it can just run through the expression from left to right and run operations as it encounters them.

To convert the expression from infix to postfix notation, we use an algorithm written by **Edsger Dijkstra** called the **shunting yard algorithm**.

Imagine our expression in infix notation traveling down a rail towards a train yard. We know that certain operators should come before others, their **precedence**, and that anything in parentheses should come first, or really, before the operations around it.

If we had another track, we could hold operators there until they were ready to be moved to our output, just like how some shunting yards sort train cars. This is what we will do to process our infix expression using a stack and a queue.

#### Aside: What in the Hell Are Stacks and Queues?

For those of you reading this that have never heard of a stack or a queue (for the record, you're in luck, I wrote this with you in mind), here's a short summary.

When we have data we want to organize, there are many different ways we may organize it. For example, you may have heard of a list, a hash map, a vector, etc. These are collectively called **data structures,** and they determine how we get to work with data. 

Two data structure we may use are called **stacks** and **queues**, and you might be able to guess what they do, or rather, what they don't do, based on their names, but basically, a stack only lets you place and remove items from the "top" (like a stack of items where the last item placed down is the first one you remove), and a queue only lets you place items at the "back", and remove items from the "front" (like a queue of people, where the first person that entered the queue is the first one that gets to leave the queue).

Of course, implementations of these data structures are often more complex and use other functions besides these, but for the sake of understanding the algorithms here, that's all you really need to remember. A stack is LIFO (last in, first out); a queue is FIFO (first in, first out).

#### End of Aside

So, returning to our shunting yard, we can lay out how our algorithm will work. We will iterate through all of the tokens in our infix expression, and  for every token:
* if it is a number, we will immediately put it next in line in a queue that will hold our postfix expression.
* if it is an operator, we put it in a stack that will hold all the operators waiting to be added to the queue.
  * but first, if the operator at the top of the stack has higher or equal precedence than the one we are processing, we will move that operator to the output queue and any other operators below it that are of higher or equal precedence.
* if it is an opening parenthesis, we will put the opening parenthesis on the stack.
* if it is a closing parenthesis, we will put all of the operators on the stack onto our queue until we find the matching open parenthesis on the stack.
* this continues until we reach the end of our expression and all tokens are processed.

There is one more thing that we need to consider: **associativity.**

Associativity determines how operators are grouped when repeated. For example, subtraction is left-associative, because when it is repeated, we group starting from the left. In other words, something like `10 - 8 - 2` = `(10 - 8) - 2`, but `10 - (8 - 2)` gives us a different result. On the other hand, exponentiation and negation are right-associative, because they group from the right. For example, `--5 = -(-5)`. If we didn't make this distinction between left-association and right-association, and we had something like `3 + --5`, our parsing algorithm would encounter a strange logic error where instead of the 5 getting negated twice, both the 3 and 5 would be negated once, giving us `-8` instead of `8` as our answer.

To solve this, if we see a right-associative operation, it must be of strictly higher precedence (not higher or equal).

As a simple example, say we want to parse the expression `5 * (7 - 1) / 2`. The following steps would be followed (where | | is our stack, () our queue, and [] what is left in our expression):

```
1. put 5 in queue                            | | [* (7 - 1) / 2]
(5) <-

2. put * on stack                            |*| <- [(7 - 1) / 2]
(5)

                                             |(| <- [7 - 1) / 2]
3. put ( on stack                            |*| 
(5)

                                             |(| [- 1) / 2]
4. put 7 in queue                            |*| 
(5 7) <-

                                             |-| <- [1) / 2]
                                             |(|
5. put - on stack                            |*|
(5 7)

                                             |-| [) / 2]
                                             |(|
6. put 1 in queue                            |*|
(5 7 1) <-
                                              
7. closing parenthesis, pop until opening    |*| [/ 2]
(5 7 1 -) <-

8. mult. has equal precedence to /, pop it   | | [/ 2]
(5 7 1 - *) <-

9. put / on stack                            |/| <- [2]
(5 7 1 - *)

10. put 2 in queue                           |/| []
(5 7 1 - * 2) <-

11. end of expression, pop stack until empty | | []
(5 7 1 - * 2 /)
```

After running this algorithm, we will have a queue that represents our infix expression in postfix notation, where each member of the queue is a character in our postfix notation.

### Calculation

It was mentioned earlier that the postfix notation we converted our expression into makes it easier to calculate the expression for a machine, but we didn't really get into that beyond "reading things left to right is easy". To be exact, it lets us calculate the result of any postfix expression using a stack-based calculator.

A stack-based calculator evaluates expressions simply: if the program sees a number, it gets pushed onto a stack. If it sees an operator, it pops numbers from the stack (depending on the arity of the operation; remember, that's how many operands an operation takes) and performs an operation on them, finally pushing the result to the top of the stack. 

Take something in infix notation like `3 * -9 + 2`. Our parser would convert it to `3 9 ~ * 2 +`. Then, to evaluate this, it would do the following operations:

```
                         |   |
                         |   |
1. push 3 onto the stack |3  |

                         |   |
                         |9  |
2. push 9 onto the stack |3  |

                         |   |
                         |-9 |
3. run negation          |3  |

                         |   |
                         |   |
4. run multiplication    |-27|

                         |   |
                         |2  |
5. push 2 onto the stack |-27|

                         |   |
                         |   |
6. run addition          |-25|
```

At the end of our calculations, the number remaining in the stack is our answer. Think of it as breaking down our big expression into a bunch of smaller operations that all eventually coalesce into the ultimate answer.

### Uncorrecting

Now this is  the fun part! If "funny mode" is turned on in our calculator, we do one final function call I like to call "uncorrecting". There are two main types of uncorrecting we do: one for numbers, and one for strings (like when we catch an error)

For numbers (and this is what's at the heart of Wyatt's idea), we basically generate a normal distribution around the number and pick a random number from that distribution. Of course, the shape of that normal distribution is different for every number, and we have a minimum distance we like to keep, but that's the gist of it.

For a string, we basically pick 1 position for every 4 characters in the string at random to replace with a different random character. Of course, we don't pick the first character, and theoretically our function could pick the same position multiple times and replace it with the same character, but that's the gist of it.

## The Frontend

I don't have much to say on the frontend, to be honest. It's just a generic Tkinter application. I will highlight this line of code that I took from a project me and Wyatt collaborated on with some other friends recently. It's the one line of code in the project I didn't write:
```py
ttk.Style().configure(event.widget.winfo_class(), wraplength=(event.widget.winfo_width() - 10))  # this line of code derived from one written by wyatt ballweber
```
It should be around line 100 in `main.py` if you're at all interested in seeing it.

## Closing Remarks

I hope this README was informative and not too confusing. Representing algorithms in Markdown is hard! Maybe I should have just used images. Anyway, if you have any questions or suggestions, feel free to DM me on Discord at @manicmaniac_.