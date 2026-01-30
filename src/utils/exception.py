import sys

class CustomException(Exception):
    def __init__(self, error_message: Exception, sys_info=sys):
        self.error_message = error_message
        _, _, tb = sys_info.exc_info()

        self.line_no = tb.tb_lineno if tb else "Unknown"
        self.file_name = tb.tb_frame.f_code.co_filename if tb else "Unknown"

        super().__init__(self.error_message)

    def __str__(self):
        return f"Error in {self.file_name} at line {self.line_no} : {self.error_message}"
