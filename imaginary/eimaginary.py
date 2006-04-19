
from twisted.cred import error

# Authentication errors
class BadPassword(error.UnauthorizedLogin):
    pass

class NoSuchUser(error.UnauthorizedLogin):
    pass


# Base Imaginary error
class ImaginaryError(Exception):
    pass


# Input handling errors
class NoSuchCommand(ImaginaryError):
    """
    There is no command like the one you tried to execute.
    """

class AmbiguousArgument(ImaginaryError):
    """
    One or more of the inputs specified can not be narrowed down to
    just one thing.  This can be due to the presence of multiple
    things with similar names, or due to the absence of anything named
    similarly to the given input.

    @ivar action: The action which was being processed when an ambiguity was
    found.

    @type part: C{str}
    @ivar part: The part of the command which was ambiguous.
    Typically something like 'target' or 'tool'.

    @type partValue: C{str}
    @ivar partValue: The string which was supplied by the user for the indicated part.

    @type objects: C{list} of C{IThing}
    @ivar objects: The objects which were involved in the ambiguity.
    """

    def __init__(self, action, part, partValue, objects):
        ImaginaryError.__init__(self)
        self.action = action
        self.part = part
        self.partValue = partValue
        self.objects = objects

# Game logic errors
class DoesntFit(ImaginaryError):
    """
    An object tried to go into a container, but the container was full.
    """


class Closed(ImaginaryError):
    """
    An object tried to go into a container, but the container was closed.
    """


class CannotMove(ImaginaryError):
    """
    An object tried to move but it was not portable so it couldn't.
    """