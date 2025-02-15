from queue import Queue


class SharedQueue:
    """SharedQueue class is used to share data between different threads."""

    def __init__(self) -> None:
        """Initialize SharedQueue class"""
        self.__signal_q = Queue()
        self.__speech_q = Queue()
        self.__morpheme_q = Queue()

    def get_from_signal_q(self) -> str:
        """Get data from signal queue"""
        return self.__signal_q.get()
    
    def put_to_signal_q(self, data) -> None:
        """Put data to signal queue"""
        self.__signal_q.put(data)

    def get_from_speech_q(self) -> str:
        """Get data from speech queue"""
        return self.__speech_q.get()
    
    def put_to_speech_q(self, data) -> None:
        """Put data to speech queue"""
        self.__speech_q.put(data)

    def get_from_morpheme_q(self) -> str:
        """Get data from morpheme queue"""
        return self.__morpheme_q.get()
    
    def put_to_morpheme_q(self, data) -> None:
        """Put data to morpheme queue"""
        self.__morpheme_q.put(data)

    def done_signal_q(self) -> None:
        """Mark signal queue as done"""
        return self.__signal_q.task_done()
    
    def done_speech_q(self) -> None:
        """Mark speech queue as done"""
        return self.__speech_q.task_done()
    
    def done_morpheme_q(self) -> None:
        """Mark morpheme queue as done"""
        return self.__morpheme_q.task_done()
    
    def join_signal_q(self) -> None:
        """Join signal queue"""
        return self.__signal_q.join()
    
    def join_speech_q(self) -> None:
        """Join speech queue"""
        return self.__speech_q.join()
    
    def join_morpheme_q(self) -> None:
        """Join morpheme queue"""
        return self.__morpheme_q.join()
    
    def join(self) -> None:
        """Join all queues"""
        self.join_signal_q()
        self.join_speech_q()
        self.join_morpheme_q()