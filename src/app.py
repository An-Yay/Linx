import socket

class URL:
    def __init__(self, url):
        self.scheme, url = url.split("://",1)
        assert self.scheme=="http"

        if "/" not in url:
            url=url+"/"

        self.host, url = url.split("/",1)
        self.path = "/"+url
    
    def request(self):
        
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP,)

        sock.connect((self.host,80))
        request="GET {} HTTP/1.0\r\n".format(self.path)
        request+="HOST: {}\r\n".format(self.host)
        request+="\r\n"

        sock.send(request.encode("utf8"))

        response = sock.makefile("r", encoding="utf8", newline="\r\n")

        statusLine = response.readline
        version, status, explanation = statusLine.split(" ",2)









url=URL("http://example.com/abc.html")
print("The url scheme is: ",url.scheme)
print("The host is: ",url.host)
print("The path is: ",url.path)
