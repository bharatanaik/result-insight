class InvalidCaptcha(Exception):
    """
    Raised when the vtu server captcha code is invalid
    """
    pass

class SerialNumberNotAvailable(Exception):
    """
    Raised when usn is University Seat Number is not available or Invalid..!
    """

class RevalNotApplied(Exception):
    """
    Raised when revaluation is not applied
    You have not applied for reval or reval results are awaited !!!
    """
    pass

