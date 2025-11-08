from core.modify_function import ReflectFunction, ShiftFunction, StretchFunction, DifferentiateFunction
from core.queue import Queue
from core.function import Function 
from core.transformations_entry import enqueueTransformations
from core.ast import copyAST

class TransformManager:
    """
    Manages a function and queue of transformations to be applied

    Responsible for executing the transformations in the correct order
    """
    def __init__(self, input_expression):
        self.transformations_queue = Queue(6)
        self.original_function = input_expression
        self.current_function = input_expression

    def addTransformations(self, x_stretch_box, y_stretch_box, x_shift_box, y_shift_box, x_reflect, y_reflect):
        """"
        Adds given transformations to the transformations queue
        """
        self.transformations_queue = enqueueTransformations(
            x_stretch_box, y_stretch_box, x_shift_box, y_shift_box, x_reflect, y_reflect
        )

    def applyTransformation(self, transformation, update_base=True):
        """
        Applies a given transformation to the current function
        """
        modifier = None

        if transformation.type == "shift":
            modifier = ShiftFunction(self.current_function, transformation.axis, transformation.value)
        elif transformation.type == "stretch":
            modifier = StretchFunction(self.current_function, transformation.axis, transformation.value)
        elif transformation.type == "reflect":
            modifier = ReflectFunction(self.current_function, transformation.axis)
        elif transformation.type == "differentiate":
            modifier = DifferentiateFunction(self.current_function)

        if modifier:
            new_func = modifier.ModifyFunction()
            if update_base:
                self.current_function = new_func
            return new_func

    def applyAllTransformations(self, graph_plotter):
        """
        Applies each transformation in the queue one after another
        """
        while not self.transformations_queue.isEmpty():
            transformation = self.transformations_queue.dequeue()
            new_func = self.applyTransformation(transformation)
            graph_plotter.plotSubsequent(new_func)

        # Resets the queue once the transformations have been applied
        self.transformations_queue = Queue(6)

    def getCurrentFunction(self):
        """
        Returns the current function
        """
        return self.current_function
            
    def nextTransformation(self):
        """
        Apply the next transformation in the queue and return the new function
        """
        if self.transformations_queue.isEmpty():
            return None
        
        # Get the transformation
        transformation = self.transformations_queue.dequeue()

        # Create a copy of the current function to modify
        ast_copy = copyAST(self.current_function.getFunction())
        var_copy = self.current_function.getVariable()
        new_func = Function(ast_copy, var_copy)

        modifier = None
        # Create an instance of the relevant modifier class 
        if transformation.getType() == "shift":
            modifier = ShiftFunction(new_func, transformation.getAxis(), transformation.getVal())
        elif transformation.getType() == "stretch":
            modifier = StretchFunction(new_func, transformation.getAxis(), transformation.getVal())
        elif transformation.getType() == "reflect":
            modifier = ReflectFunction(new_func, transformation.getAxis())
        elif transformation.getType() == "differentiate":
            modifier = DifferentiateFunction(new_func)

        if modifier:
            # Create a new function from the modifier and store as the current function
            self.current_function = modifier.ModifyFunction()
            return self.current_function
        return None

    def setBaseFunction(self, new_function):
        """
        Set a modified function as the new base function
        This is for implementation in repeated differentiation for further derivatives
        """
        self.current_function = new_function
        self.transformations_queue = Queue(1)

    def hasTransformations(self):
        return not self.transformations_queue.isEmpty()
        
