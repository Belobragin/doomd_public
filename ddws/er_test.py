from hardcode import get_error_essence

test_err =\
r"HTTPConnectionPool(host='localhost', port=8006):\
    Max retries exceeded with url: /alterit/?algo_name=bim\
    (Caused by NewConnectionError('<urllib3.connection.HTTPConnection\
    object at 0x7f2ba966ff40>: Failed to establish a new connection:\
    [Errno 111] Connection refused'))"

print(get_error_essence(test_err))