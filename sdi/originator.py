class Originator(ABC):
     
    def options(self):
        """
        Return list of options strings.
        """
        pass

    def arguments(self):
        """
        Return list of argument string.
        """
        pass

    def command(self):
        """
        Return text of command.
        """
        pass

    def help(self):
        """
        Return help text.
        """
        pass

    def __call__(self):
        """
        The main function goes here.
        """

    def __init__(self):
        """
        Do the heavy lifting of applying appropriate click decorators +
        using function introspection to come up with good defaults.
        """
        pass
