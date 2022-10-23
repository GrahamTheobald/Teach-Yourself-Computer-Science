"""
4. (9 points) Digital
(a) (3 pt) Implement collapse, which takes a non-negative integer, and returns the result of removing all digits from it that duplicate the digit immediately to their right.
"""


def collapse(n):
    """For non-negative N, the result of removing all digits that are equal
    to the digit on their right, so that no adjacent digits are the same.
    >>> collapse(1234)
    1234
    >>> collapse(12234441)
    12341
    >>> collapse(0)
    0
    >>> collapse(3)
    3
    >>> collapse(11200000013333)
    12013
    """
    left, last = n // 10, n % 10
    if n < 10:
        return last
    elif left % 10 == last:
        return collapse(left)
    else:
        return collapse(left) * 10 + last


"""
(b) (6 pt) Implement find_pair, which takes a two-argument function, p, as input and returns another function.
The returned function takes a non-negative integer n; it returns True if and only if p returns a true value
when called on at least one pair of adjacent digits in n, and False otherwise.
"""


def find_pair(p):
    """Given a two-argument function P, return a function that takes a
    non-negative integer and returns True if and only if two adjacent digits
    in that integer satisfy P (that is, cause P to return a true value).
    >>> z = find_pair(lambda a, b: a == b) # Adjacent equal digits
    >>> z(1313)
    False
    >>> z(12334)
    True
    >>> z = find_pair(lambda a, b: a > b)
    >>> z(1234)
    False
    >>> z(123412)
    True
    >>> find_pair(lambda a, b: a <= b)(9753)
    False
    >>> find_pair(lambda a, b: a == 1)(1) # Only one digit; no pairs.
    False
    """
    def find(n):
        while n >= 10:
            if p(n // 10, n % 10):
                return False
            else:
                n = n // 10
        return False

    return find


"""
5. (6 points) Won’t You Be My Neighbor?
(a) (4 pt) Write repeat_digits, which takes a positive integer n and returns another integer that is identical to
n but with each digit repeated.

(b) (2 pt) Let d be the number of digits in n. What is the runtime of repeat_digits with respect to d?
# Θ(1) # Θ(log d) # Θ(√
d) # Θ(d) # Θ(d
2
) # Θ(2d
)
"""


def repeat_digits(n):
    """Given a positive integer N, returns a number with each digit repeated.
    >>> repeat_digits(1234)
    11223344
    """
    last, rest = n % 10, n // 10
    if n < 10:
        return last * 11
    return repeat_digits(rest) * 100 + last * 11


"""
6. (20 points) Palindromes
Definition. A palindrome is a sequence that has the same elements in normal and reverse order.
(a) (3 pt) Implement pal, which takes a positive integer n and returns a positive integer with the digits of
n followed by the digits of n in reverse order.
Important: You may not write str, repr, list, tuple, [, or ].
"""


def pal(n):
    """Return a palindrome starting with n.
    >>> pal(12430)
    1243003421
    """
    m = n
    while m:
        n, m = n * 10 + m % 10, m // 10
    return n


"""
(b) (4 pt) Implement contains, which takes non-negative integers a and b. It returns whether all of the
digits of a also appear in order among the digits of b.
Important: You may not write str, repr, list, tuple, [, or ].
"""


def contains(a, b):
    """Return whether the digits of a are contained in the digits of b.
    >>> contains(357, 12345678)
    True
    >>> contains(753, 12345678)
    False
    >>> contains(357, 37)
    False
    """
    if a == b:
        return True
    if a > b:
        return False
    if a % 10 == b % 10:
        return contains(a // 10, b // 10)
    else:
        return contains(a, b // 10)
