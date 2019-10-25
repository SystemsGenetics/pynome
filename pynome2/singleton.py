"""
todo
"""






def singleton(class_):
    """
    todo
    """
    # Initialize the dictionary of singleton instances.
    instances = {}
    # Create a wrapper that returns instances using the dictionary.
    def wrapper():
        # If the class does not have an instance then create one.
        if class_ not in instances: instances[class_] = class_()
        # Return the singleton instance.
        return instances[class_]
    # Return the wrapper function.
    return wrapper
