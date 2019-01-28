import socket
import protocol
import sys
import signal
import shutil
from os import walk

server_addr = "localhost"
server_port = 1234
server_datadir = "data/"


def main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((server_addr, server_port))
    s.listen(5)

    def clean_exit(signal, frame):
        print "ctrl+c pressed"
        s.close()
        sys.exit()

    # when ctrl+c is pressed, call clean_exit function
    signal.signal(signal.SIGINT, clean_exit)

    while True:
        client, (client_addr, client_port) = s.accept()
        print "client connected from %s" % client_addr

        try:
            (method, bodylen, methodparams) = protocol.read_header(client)
            body = ""
            if bodylen > 0:
                body = protocol.read_body(client, bodylen)
            request = protocol.Message(method, methodparams, body)
            response = handle_request(request, client)
            protocol.send_message(response, client)
        except protocol.InvalidMethodException:
            print "received invalid method from %s, disconnecting the client..." % (client_addr)
        except protocol.MalformedHeaderException:
            print "received malformed header the %s, disconnecting the client" % (client_addr)

        client.close()


def handle_request(request, client):
	if request.method == "LIST":
	
		with open("D:\\testi.txt") as f:
			f = f.read().splitlines()
			body = "\r\n".join(f)
			response = protocol.Message("LISTRESPONSE", len(f), body)
			return response

	elif request.method == "DOWNLOAD":
		filename = request.methodparams[0]
		print filename
		try:
			with open("D:\\testi.txt", "a") as myfile:
				myfile.write(filename+'\n')
            # inefficient, but works for now
			body = "Ok"
			response = protocol.Message("FILE", filename, body)
			return response

		except Exception as e:
			print e
			error_response = protocol.Message("ERROR", protocol.ERROR_FILENOTFOUND, "") 
			return error_response
	elif request.method == "DELETE":
		filename = request.methodparams[0]
		numero = int(filename)
		print numero
		try:
			
			with open("D:\\testi.txt") as f:
				lines = f.read().splitlines()
				
			print lines
			numero = numero -1
			lines.pop(numero)
			print lines
			#split() splittina \n, parseta 
			
			
			x = open("D:\\testi.txt", 'w')
			for item in lines: 
				x.write(item + "\n")
			x.close()
            # inefficient, but works for now
			body = "Ok"
			response = protocol.Message("DELETERESPONSE", filename, body)
			return response

		except Exception as e:
			print e
			error_response = protocol.Message("ERROR", protocol.ERROR_FILENOTFOUND, "") 
			return error_response
	else:
		raise protocol.UnexpectedMethodException(request.header)

if __name__ == "__main__":
    main()
