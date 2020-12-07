class SwagmanException(Exception):
    pass

class RequestParserException(SwagmanException):
    pass

class ResponseParserException(SwagmanException):
    pass

class CollectionParserException(SwagmanException):
    pass

class FolderParserException(SwagmanException):
    pass

class RequestItemParserException(SwagmanException):
    pass