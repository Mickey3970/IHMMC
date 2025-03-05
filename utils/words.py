import time

class WordBuilder:
    def __init__(self, word_timeout=2):
        self.current_word = ""
        self.word_timeout = word_timeout
        self.last_update = time.time()
    
    def add_gesture(self, gesture):
        current_time = time.time()
        
        if gesture == "UNDO":
            if self.current_word:
                self.current_word = self.current_word[:-1]
            return self.current_word
        
        if current_time - self.last_update > self.word_timeout:
            self.current_word = ""
        
        self.current_word += gesture
        self.last_update = current_time
        
        return self.current_word