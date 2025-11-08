from core.transformations import reflectXAxis, reflectYAxis, shiftX, shiftY, stretchX, stretchY
from core.differentiation import differentiate

# Base class for all types of function modification
# Transformation classes inherit from ModifyFunction and implement polymorphism on its methods
class ModifyFunction:
    def __init__(self, altered_function):
        self.altered_function = altered_function 

    def ModifyFunction(self):
        # Base method for all function modifications
        # Just returns the function
        return self.altered_function

class DifferentiateFunction(ModifyFunction):
    def ModifyFunction(self):
        """
        Applies differentiation to the function AST
        """
        new_tree = differentiate(self.altered_function.getFunction())
        if new_tree is None:
            return None
        self.altered_function.setFunction(new_tree)
        return self.altered_function

class ShiftFunction(ModifyFunction):
    def __init__(self, altered_function, axis, value):
        super().__init__(altered_function)
        # Add axis and value to the constructor
        self.axis = axis
        self.value = value

    def ModifyFunction(self):
        """
        Applies a shift to the function AST
        """
        tree = self.altered_function.getFunction()
        if self.axis == "x":
            tree = shiftX(tree, self.value)
        elif self.axis == "y":
            tree = shiftY(tree, self.value)
        self.altered_function.setFunction(tree)
        return self.altered_function

class StretchFunction(ModifyFunction):
    def __init__(self, altered_function, axis, value):
        super().__init__(altered_function)
        # Add axis and value to the constructor
        self.axis = axis
        self.value = value

    def ModifyFunction(self):
        """
        Applies a stretch to the function AST
        """
        tree = self.altered_function.getFunction()
        if self.axis == "x":
            tree = stretchX(tree, self.value)
        elif self.axis == "y":
            tree = stretchY(tree, self.value)
        self.altered_function.setFunction(tree)
        return self.altered_function

class ReflectFunction(ModifyFunction):
    def __init__(self, altered_function, axis):
        super().__init__(altered_function)
        # Add axis to the constructor
        self.axis = axis

    def ModifyFunction(self):
        """
        Applies a reflection to the function AST
        """
        tree = self.altered_function.getFunction()
        if self.axis == "x":
            tree = reflectXAxis(tree)
        elif self.axis == "y":
            tree = reflectYAxis(tree)
        self.altered_function.setFunction(tree)
        return self.altered_function
