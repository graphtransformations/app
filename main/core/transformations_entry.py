from core.transformation_class import Transformation
from core.parser import tokenize
from core.queue import Queue

def validTransformation(value, type):
    """
    Performs validation on the user input depending on the type of transformation
    Utilises the tokenizer from the main function parser
    """
    contains_name = False
    
    # Only parses value if not boolean
    if type != "reflect":
        tokens = tokenize(value) 
        
        # Only check tokens if they exist
        if tokens == None:
            return False

        # If NAME pattern in value, will be rejected
        for token in tokens:
            if token[0] == "NAME":
                contains_name = True
                return False
            
   # Checking if the value is none
    if value == "":
        return False
    
    # Checking if the value is default, if so the transformation should be skipped
    try:
        if not contains_name:
            if type == "shift" and eval(value) == 0:
                return False
            elif type == "stretch" and eval(value) == 1:
                return False
            elif type == "reflect" and value is False:
                return False
            
            # Checking if stretching by scale factor 0
            elif type == "stretch" and eval(value) == 0:
                return False
            else:
                return True
    except:
        return False
    return False

def enqueueTransformations(x_stretch_box, y_stretch_box, x_shift_box, y_shift_box, x_reflect, y_reflect):
    """
    Enqueues the transformations that are valid
    """
    transformations_queue = Queue(6)

    # Read values from input boxes
    stretchX_value = x_stretch_box.getText()
    stretchY_value = y_stretch_box.getText()
    shiftX_value = x_shift_box.getText()
    shiftY_value = y_shift_box.getText()
    reflectX_bool = x_reflect.getValue()
    reflectY_bool = y_reflect.getValue()

    # X-axis
    if validTransformation(stretchX_value, "stretch"):
        transformations_queue.enqueue(Transformation("stretch", eval(stretchX_value.replace("^", "**")), 'x'))
    if validTransformation(reflectX_bool, "reflect"):
        transformations_queue.enqueue(Transformation("reflect", reflectX_bool, 'x'))
    if validTransformation(shiftX_value, "shift"):
        transformations_queue.enqueue(Transformation("shift", eval(shiftX_value.replace("^", "**")), 'x'))

    # Y-axis
    if validTransformation(stretchY_value, "stretch"):
        transformations_queue.enqueue(Transformation("stretch", eval(stretchY_value.replace("^", "**")), 'y'))
    if validTransformation(reflectY_bool, "reflect"):
        transformations_queue.enqueue(Transformation("reflect", reflectY_bool, 'y'))
    if validTransformation(shiftY_value, "shift"):
        transformations_queue.enqueue(Transformation("shift", eval(shiftY_value.replace("^", "**")), 'y'))

    return transformations_queue
        