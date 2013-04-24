JOB_COMPLETE_TIME = 10

class Job():
    
    def __init__(self):
        
        self.time = 0
        
    def run(self):
        
        self.time += 1
        
    def isEnd(self):
        
        return self.time == JOB_COMPLETE_TIME
    
class JobQueue():
    
    def __init__(self):
        
        self.queue = []
        
    def add(self, job):
        
        self.queue.append()
        