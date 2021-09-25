from .web_elem import WebElem

class ClickableElem(WebElem):
    def click(self, timeout=100):
        elem = self.wait_for_load(timeout)
        elem.click()