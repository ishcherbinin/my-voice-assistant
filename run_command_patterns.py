class AbstractCommandPatterns:
    EXIT_COMMAND = None

class RuCommandPatterns(AbstractCommandPatterns):
    EXIT_COMMAND = "завершить"



def patter_resolver(pattern_identifier: str) -> AbstractCommandPatterns:
    """
    Return the command patterns based on the pattern identifier.
    :param pattern_identifier:
    :return:
    """
    match pattern_identifier:
        case "ru":
            return RuCommandPatterns()
        case _:
            return AbstractCommandPatterns()
