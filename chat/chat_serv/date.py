def get_date():
    from datetime import datetime

    now = datetime.now()
    current_date = now.strftime('%Y_%m_%d_%H_%M_%S') + f'_{int(now.microsecond / 1000):03d}'
    return current_date