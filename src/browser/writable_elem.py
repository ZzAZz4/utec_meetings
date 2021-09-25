from .web_elem import WebElem


class WritableElem(WebElem):
    def __set__(self, obj, value):
        """Sets the text to the value supplied"""

        elem = self.wait_for_load()
        elem.clear()
        elem.send_keys(value)

    def __get__(self, obj, owner):
        """Gets the text of the specified object"""
        
        element = self.wait_for_load()
        return element.get_attribute("value")