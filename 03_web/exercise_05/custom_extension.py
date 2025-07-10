from burp import IBurpExtender, IHttpListener
import re

class BurpExtender(IBurpExtender, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("API Key Scanner")
        callbacks.registerHttpListener(self)
        print("[*] API Key Scanner loaded")

        # Define API key patterns
        self.api_key_patterns = {
            "AWS Access Key": re.compile(r'AKIA[0-9A-Z]{16}'),
            "Google API Key": re.compile(r'AIza[0-9A-Za-z\-_]{35}'),
            "Slack Token": re.compile(r'xox[baprs]-[0-9a-zA-Z]{10,48}'),
            "Bearer Token": re.compile(r'Bearer\s+[A-Za-z0-9\-._~+/]+=*'),
        }

    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        # Only look at responses
        if messageIsRequest:
            return

        response = messageInfo.getResponse()
        if not response:
            return

        responseInfo = self._helpers.analyzeResponse(response)
        headers = responseInfo.getHeaders()
        body = response[responseInfo.getBodyOffset():].tostring()

        # Scan for API key patterns
        for key_type, pattern in self.api_key_patterns.items():
            for match in pattern.findall(body):
                print("[!] Found {}: {}".format(key_type, match))
                # Highlight the request in Burp (optional)
                messageInfo.setHighlight("red")
                messageInfo.setComment("API Key detected: {}".format(key_type))
