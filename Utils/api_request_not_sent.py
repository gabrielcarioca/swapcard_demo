class APIRequestNotSent(Exception):
    """Exception raised when an expected API request was not sent in the current page

    Attributes:
        message -- explaining which expected API request was not sent in the expected page
    """

    def __init__(self, message="Expected request to be sent not found in current page"):
        self.message = message
        super().__init__(self.message)
