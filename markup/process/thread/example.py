import threading

class ThreadingExample(object):
    
    def __init__(self, app):  
        thread = threading.Thread(target=app.run, args=())
        thread.daemon = True                            
        thread.start()  
