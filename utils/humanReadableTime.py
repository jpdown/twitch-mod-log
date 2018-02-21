def time(seconds):
    """Function to convert seconds to human readable time"""
    days = seconds // 86400
    hours = seconds // 3600 % 24
    minutes = seconds // 60 % 60
    seconds = seconds % 60
    #Create message string
    message = ""
    if days != 0:
        message += "{0} Days ".format(days)
    if hours != 0:
        message += "{0} Hours ".format(hours)
    if minutes != 0:
        message += "{0} Minutes ".format(minutes)
    if seconds != 0:
        message += "{0} Seconds".format(seconds)
    return(message)