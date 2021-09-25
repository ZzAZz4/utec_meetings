def wired_func(request_func, previous_callback):
    def call(*args, **kwargs):
        if callable(request_func):
            request_func(*args, **kwargs)
        if callable(previous_callback):
            previous_callback(*args, **kwargs)
            
    return call

class Wiretap:
    """Implements a self-cleaning wrapper aroud the seleniumwire interceptor interface.
    Concatenation of multiple wiretaps results in sequential execution of all callbacks."""
    
    def __init__(self, driver, request_callback=None, response_callback=None):
        self.request_callback = request_callback
        self.response_callback = response_callback
        self.driver = driver
        
        self.save = (driver.request_interceptor, driver.response_interceptor)

    def __enter__(self):
        self.activate()
        return self.driver

    def __exit__(self, exc_type, exc_value, tb):
        self.deactivate()
        if exc_type is not None:
            from traceback import print_exception
            print_exception(exc_type, exc_value, tb)
            raise exc_type(exc_value).with_traceback(tb)

    def activate(self):
        prev_request_callback, prev_response_callback = self.save
        
        self.driver.request_interceptor = wired_func(
            self.request_callback, 
            prev_request_callback)
        
        self.driver.response_interceptor = wired_func(
            self.response_callback, 
            prev_response_callback)
    
    def deactivate(self):
        prev_request_callback, prev_response_callback = self.save
        if prev_request_callback is None:
            del self.driver.request_interceptor 
        else:
            self.driver.request_interceptor = prev_request_callback
            
        if prev_response_callback is None:
            del self.driver.response_interceptor
        else:
            self.driver.response_interceptor = prev_response_callback