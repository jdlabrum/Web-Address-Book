import http.server

def RunHTTPServer(server="", port=8080):
     http.server.test(HandlerClass=http.server.CGIHTTPRequestHandler, bind=server, port=port)
     
if __name__ == '__main__':
     RunHTTPServer("127.0.0.1", 8080)
     #http.server.test(myRequestHandler, http.server)