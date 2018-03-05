


def get_err_resp(message):
    """Error dict"""
    return dict(success=False,
                message=message)


def get_ok_resp(message, data=None):
    """Error dict"""
    if data:
        return dict(success=True,
                    message=message,
                    data=data)

    return dict(success=True,
                message=message)
