
VALIDMETHODS = [
        "LIST",
        "LISTRESPONSE",
        "DOWNLOAD",
        "FILE",
        "ERROR",
		"DELETE",
		"DELETERESPONSE"
        ]

ERROR_BADFOLDER = 1
ERROR_NOTAFILE = 2
ERROR_FILENOTFOUND = 3

class Message:

    def __init__(self, method, methodparams, body):
        if method not in VALIDMETHODS:
            raise InvalidMethodException()

        self.method = method
        self.methodparams = methodparams
        self.body = body
        self.bodylen = len(body)


def read_header(client):
    header = read_until_newline(client).strip()
    parts = header.split(" ")

    # There are no messages in the protocol that do not have method parametrs.
    # This means that there are always atleast 3 words in the header
    if len(parts) < 3:
        raise MalformedHeaderException()

    method = parts[0]
    try:
        bodylen = int(parts[1])
    except TypeError:
        raise MalformedHeaderException("bodylen '' is not a number" % parts[1])
    methodparams = parts[2:]

    return (method, bodylen, methodparams)

def read_until_newline(client):
    line = ""
    while "\n" not in line:
        c = client.recv(1)
        if c == "":
            break
        line += c
    return line


def read_body(client, bodylen):
    body = ""

    while len(body) < bodylen:
        data = client.recv(1024)
        # empty body or client disconnected
        if data == "":
            break
        body += data

    return body


def send_message(message, client):
    data = "%s %d %s\r\n%s" % (message.method,
            message.bodylen,
            message.methodparams,
            message.body)
    client.sendall(data)


class InvalidMethodException(Exception):

    def __init__(self, *args):
        msg = "Invalid method exception"
        self.message = msg
        super(InvalidMethodException, self).__init__(msg, args)


class MalformedHeaderException(Exception):

    def __init__(self, *args):
        msg = "MalformedHeaderException"
        self.message = msg
        super(MalformedHeaderException, self).__init__(msg, args)


class UnexpectedMethodException(Exception):

    def __init__(self, method, *args):
        msg = "Unexpected method '%s'" % method
        self.message = msg
        super(UnexpectedMethodException, self).__init__(msg, args)
