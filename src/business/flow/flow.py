from abc import ABC, abstractmethod

# todo: Add docs to each process

class IFlowManager(ABC):

    # todo: Have all these methods return a message code to send, message codes be an enum ( eg ConversationManager ? )

    # I need a method that takes in a State, and maps it to a method
    @abstractmethod
    def start(self) : ...

    @abstractmethod
    def get_lang(self): ...

    @abstractmethod
    def get_service(self): ...

    @abstractmethod
    def get_service_bv(self): ...

    @abstractmethod
    def get_city(self): ...

    @abstractmethod
    def get_dim(self): ...

    @abstractmethod
    def get_activity(self): ...

    @abstractmethod
    def complete(self): ...

    @abstractmethod
    def unexpected(self): ...





