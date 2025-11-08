from core.ast import ASTNode
import math 

def reflectXAxis(node):
    """
    Reflects the function across the X-axis by multiplying the whole expression by -1
    """
    if node is None:
        return None
    negative_one = ASTNode("NUMBER", "-1", None, None)
    return ASTNode("OP", "*", negative_one, node)


def reflectYAxis(node):
    """
    Reflects the function across the Y-axis by multiplying variables by -1
    """
    if node is None:
        return None
    elif node.type == "NAME":
        negative_one = ASTNode("NUMBER", "-1", None, None)
        return ASTNode("OP", "*", negative_one, node)
    else:
        # Recursively reflect left and right subtrees
        if node.left:
            node.left = reflectYAxis(node.left)
        if node.right:
            node.right = reflectYAxis(node.right)
        return node


def shiftX(node, shift):
    """
    Shifts the function along the X-axis by subtracting the shift value 
    """
    if node is None:
        return None
    elif node.type == "NAME":
        shift_amount = ASTNode("NUMBER", str(shift), None, None)
        return ASTNode("OP", "-", node, shift_amount)
    else:
        if node.left:
            node.left = shiftX(node.left, shift)
        if node.right:
            node.right = shiftX(node.right, shift)
        return node



def shiftY(node, shift):
    """
    Shifts the function along the Y-axis by adding the shift value to the expression
    """
    if node is None:
        return None
    shift_amount = ASTNode("NUMBER", str(shift), None, None)
    return ASTNode("OP", "+", node, shift_amount)


def stretchX(node, stretch):
    """
    Stretches the function along the X-axis by dividing by the stretch
    """
    if node is None:
        return None
    elif node.type == "NAME":
        factor = ASTNode("NUMBER", str(stretch), None, None)
        return ASTNode("OP", "/", node, factor)
    else:
        if node.left:
            node.left = stretchX(node.left, stretch)
        if node.right:
            node.right = stretchX(node.right, stretch)
        return node


def stretchY(node, stretch):
    """
    Stretches the function along the Y-axis by multiplying by the stretch
    """
    if node is None:
        return None
    factor = ASTNode("NUMBER", str(stretch), None, None)
    return ASTNode("OP", "*", factor, node)
