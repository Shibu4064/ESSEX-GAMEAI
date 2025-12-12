import math

class Vector2D:
    # Vector2D class for Python 3
    # Original version from Learning Scientific Programming with Python, Second Edition, by Christian Hill, (ISBN: 9781108745918) in December 2020
    # This version overloads the operators +,-,* etc to allow them to work with
    # Vector2D operations.  See e.g. https://www.geeksforgeeks.org/operator-overloading-in-python/ for
    # an introduction to operator overloading in Python3.

    def __init__(self, x, y):
        # constructor method
        self.x, self.y = x, y

    def __str__(self):
        # Human-readable string representation of the vector.
        return '({:g},{:g})'.format(self.x, self.y)

    def dot(self, other):
        # The scalar product (dot product) of self and other. Both must be vectors.
        # raise Exception("Not Implemented")
        if not isinstance(other, Vector2D):
            raise TypeError('Can only take dot product of two Vector2D objects')
        return self.x * other.x + self.y * other.y # TODO fix this line
        
    # Alias the __matmul__ method to dot so we can use a @ b as well as a.dot(b).
    __matmul__ = dot #  Overloads @ operator.

    def __sub__(self, other):
        # Vector subtraction.  Overloads - operator.
        # raise Exception("Not Implemented")
        return Vector2D(self.x - other.x, self.y - other.y) # TODO fix this line

    def __add__(self, other):
        # Vector addition.  Overloads + operator.
        # raise Exception("Not Implemented")
        return Vector2D(self.x + other.x, self.y + other.y) # TODO fix this line

    def __mul__(self, scalar):
        # raise Exception("Not Implemented")
        # Multiplication of a vector by a scalar.  Overloads * operator.
        if isinstance(scalar, int) or isinstance(scalar, float):
            return Vector2D(self.x * scalar, self.y * scalar) # TODO fix this line
        raise NotImplementedError('Can only multiply Vector2D by a scalar')

    def __rmul__(self, scalar):
        # Reflected multiplication so vector * scalar also works.
        return self.__mul__(scalar)

    def __neg__(self):  
        # Negation of the vector.  Overloads - operator.
        return Vector2D(-self.x, -self.y)

    def __truediv__(self, scalar):
        # True division of the vector by a scalar.  Overloads / operator.
        return self*(1/scalar)

    def __abs__(self):
        # Absolute value (magnitude) of the vector.  Overloads abs function.
        # raise Exception("Not Implemented")
        return math.sqrt(self.x**2 + self.y**2) # TODO fix this line

    def mag(self): # magnitude of the vector
        return abs(self)

    def normalise(self): # return a normalised copy of this vector
        length=self.mag()
        if length!=0:
            return self/length
        else:
            return self
