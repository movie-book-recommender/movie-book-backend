"""
This module implement general methods used across all classes.
"""

class Helper:
    """
    This class implements methods used across all other classes. 
    """
    def __init__(self):
        pass

    def dict_helper(self, object_list):
        """
        This method implements conversion of input into a dictionary

        Args:
            object_list (list): List of objects.

        Returns:
            Dictionary: Returns the given data in dictionary form.
        """
        return [item.object_to_dictionary() for item in object_list]

helper = Helper()
