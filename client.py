import socket
import sys
import protocol
import shutil

MAIN_MENU_CHOICE_LIST = 1
MAIN_MENU_CHOICE_DOWNLOAD = 2
MAIN_MENU_CHOICE_DELETE = 3

def main():
	if len(sys.argv) < 2:
		print "not enough parameters."
		print "usage: %s ADDRESS [PORT]"
		sys.exit(1)

	server_addr = sys.argv[1]
	server_port = 0

	if len(sys.argv) == 2:
		server_port = 1234
	else:
		server_port = int(sys.argv[2])

	while True:
		choice = main_menu()
		print "Connecting to %s:%d..." % (server_addr, server_port)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((server_addr, server_port))

		if choice == MAIN_MENU_CHOICE_LIST:
			folder = "."
			request = protocol.Message("LIST", folder, "")
			protocol.send_message(request, s)

			(method, bodylen, methodparams) = protocol.read_header(s)

			if method == "LISTRESPONSE":
				body = ""
				if bodylen > 0:
					body = protocol.read_body(s, bodylen)

				files = body.split("\r\n")
				print "files:"
				i = 1;
				for file in files:
					print i , " %s" % file
					i=i+1
			else:
				print "an error occured: %s" % methodparams[0]

		elif choice == MAIN_MENU_CHOICE_DOWNLOAD:
			filename = raw_input("filename: ")
			request = protocol.Message("DOWNLOAD", filename, "")
			protocol.send_message(request, s)

			(method, bodylen, methodparams) = protocol.read_header(s)

			if method == "FILE":
				# write the body to a file of the same name
				print "Sana lisatty"
			else:
				print "an error occured: %s" % methodparams[0]
		elif choice == MAIN_MENU_CHOICE_DELETE:
			filename = raw_input("filename: ")
			request = protocol.Message("DELETE", filename, "")
			protocol.send_message(request, s)

			(method, bodylen, methodparams) = protocol.read_header(s)

			if method == "DELETERESPONSE":
				# write the body to a file of the same name
				print "Sana poistettu"
			else:
				print "an error occured: %s" % methodparams[0]

		s.close()


def main_menu():
	print "Simple DFTP Client"
	print "1) List available files"
	print "2) Download a file"
	print "3) Delete"

	while True:
		try:
			choice = int(raw_input("Choice: "))
			if choice != MAIN_MENU_CHOICE_LIST and choice != MAIN_MENU_CHOICE_DOWNLOAD and choice != MAIN_MENU_CHOICE_DELETE:
				print "Bad choice, try again"
			return choice
		except:
			print "Not a number!, try again"



if __name__ == "__main__":
    main()
