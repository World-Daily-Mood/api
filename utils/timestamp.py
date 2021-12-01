import datetime

def get_all(data):
    if data is not None:
        return last_req(data), nex_req(data), can_req(data)

def last_req(data):
    if data is not None:
        return data [2]

def nex_req(data):
    if data is not None:
        one_day = datetime.timedelta(days=1)

        return data[2] + one_day

def can_req(data):
    if data is not None:
        next_req = nex_req(data)
        now = datetime.datetime.now()

        return next_req <= now

    else:
        return True