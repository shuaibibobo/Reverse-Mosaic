
class BaseToolClass:

    def return_tools(self)->list:
        raise Exception("Not overriden exception")
    

def get_class():
    return BaseToolClass()