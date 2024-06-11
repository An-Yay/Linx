import socket
import ssl


class URL:
    def __init__(self, url):
        """
        Initialize the URL object by parsing the input URL.
        
        Args:
        url (str): The input URL in the format 'http://host/path'.
        """
        self.scheme, url = url.split("://", 1)
        assert self.scheme in ["http", "https"]

        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            if  ":" in self.scheme:
                self.host, port = self.host.split(":", 1)
                self.port = int(port)
            self.port = 443

        if "/" not in url:
            url = url + "/"

        self.host, url = url.split("/", 1)
        self.path = "/" + url

    def request(self):
        """
        Send an HTTP GET request to the specified host and path.

        Returns:
        str: The content of the HTTP response.
        """
        # Create a socket
        sock = socket.socket(family=socket.AF_INET,
                             type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)

        
        sock.connect((self.host, self.port))
        if self.scheme == "https":
            context = ssl.create_default_context()
            sock = context.wrap_socket(sock, server_hostname=self.host)


        # Formulate the GET request
        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
        request += "\r\n"

        # Send the request
        sock.send(request.encode("utf8"))

        # Get the response
        response = sock.makefile("r", encoding="utf8", newline="\r\n")

        # Read the status line
        statusLine = response.readline()
        version, status, explanation = statusLine.split(" ", 2)

        # Read the headers
        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n":
                break

            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()

        # Ensure content is not encoded or chunked
        assert "content-encoding" not in response_headers, "Content encoding is not supported."
        assert "transfer-encoding" not in response_headers, "Transfer encoding is not supported."

        # Read the body content
        content = response.read()
        sock.close()
        return content


def show(body, filename):
    """
    Print the body of the HTTP response, ignoring HTML tags.
    
    Args:
    body (str): The body content of the HTTP response.
    """
    in_tag = False
    with open(filename, 'w', encoding='utf8') as file:

        for c in body:
            if c == '<':
                in_tag = True
            elif c == '>':
                in_tag = False
            elif not in_tag:
                file.write(c)


def load(url):
    """
    Load the content from the given URL and print it.
    
    Args:
    url (URL): The URL object to fetch the content from.
    """
    body = url.request()
    # print()
    filename = url.host.split('.')[0]+'.txt'
    show(body, filename)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python app.py [your url]")
        print()
    else:
        load(URL(sys.argv[1]))
        print("Your HTML file is ready at {}.txt".format(
            sys.argv[1].split("//")[1].split('.')[0]))
