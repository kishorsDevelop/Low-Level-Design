from abc import ABC, abstractmethod

class Handler:
    @abstractmethod
    def handle(self, level, message):
        pass

class InfoHandler(Handler):
    def __init__(self, next):
        self.next = next
    
    def handle(self, level, message):
        if level.upper() == 'INFO':
            print(f'{message} : {message}')
        else:
            self.next.handle(level, message)

class WarnHandler(Handler):
    def __init__(self, next):
        self.next = next
    
    def handle(self, level, message):
        if level.upper() == 'WARN':
            print(f'{message} : {message}')
        else:
            self.next.handle(level, message)

class ErrorHandler(Handler):
    def __init__(self, next):
        self.next = next
    
    def handle(self, level, message):
        if level.upper() == 'ERROR':
            print(f'{level} : {message}')
        else:
            self.next.handle(level, message)

class DebugHandler(Handler):
    pass

class FailureHandler(Handler):
    pass

class Logger:

    def __init__(self):
        # can be extended to debug handler and failure handler 
        errorhandler = ErrorHandler(None)
        warnhandler = WarnHandler(errorhandler)
        infohandler = InfoHandler(warnhandler)
        self.handler = infohandler

    def log(self, level, message):
        self.handler.handle(level, message)
    

if __name__ == '__main__':
    logger = Logger()
    logger.log("WARN", "Warning")
    logger.log("INFO", "Information")
    logger.log("ERROR", "Error")
