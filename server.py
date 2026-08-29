"""Small Python navigation assistant for the RTI Online prototype.
Run: python server.py
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json

RESPONSES = [
    (('file', 'submit', 'request', 'application', 'फाइल'), 'To file an RTI, choose “File an RTI Request” on the home page. The guided form collects applicant details, authority, information, documents, review and payment.', '#file'),
    (('appeal', 'first appeal', 'अपील'), 'You can start a First Appeal from the “File First Appeal” route. Keep your original application number and response details available.', '#first-appeal'),
    (('track', 'status', 'where is', 'स्थिति'), 'Use “Track Application” and enter your registration number with your registered contact details.', '#track'),
    (('history', 'past', 'my application', 'dashboard'), '“My Applications” shows your active requests, received responses, appeals and saved drafts.', '#apps'),
    (('authority', 'department', 'ministry', 'organisation', 'organization', 'public authority'), 'Use the Public Authorities directory to search by ministry, department or organisation. The assistant can suggest a route, but you should confirm the authority yourself.', '#authority'),
    (('help', 'manual', 'guide', 'how'), 'The Help Center and RTI User Manual explain filing, tracking, payment, documents and common questions.', '#help'),
    (('payment', 'pay', 'fee'), 'Payment is the final step after review. Select the configured payment method shown by the portal and never share card details in chat.', '#payment'),
]

def answer(message):
    text = message.lower()
    for words, reply, action in RESPONSES:
        if any(word in text for word in words):
            return {'reply': reply, 'action': action}
    return {'reply': 'I can help you navigate filing an RTI, filing a First Appeal, tracking an application, finding a public authority, viewing applications, payment, or the help guide. Which one do you need?', 'action': '#home'}

class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204); self.headers_out(); self.end_headers()
    def do_POST(self):
        if self.path != '/api/chat': self.send_error(404); return
        try:
            body = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))))
            result = answer(str(body.get('message', '')))
            payload = json.dumps(result).encode()
            self.send_response(200); self.headers_out(); self.send_header('Content-Type', 'application/json'); self.send_header('Content-Length', len(payload)); self.end_headers(); self.wfile.write(payload)
        except (ValueError, TypeError): self.send_error(400, 'Invalid message')
    def headers_out(self):
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:5173'); self.send_header('Access-Control-Allow-Headers', 'Content-Type'); self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')

if __name__ == '__main__':
    print('RTI navigation assistant running at http://localhost:8000')
    ThreadingHTTPServer(('localhost', 8000), Handler).serve_forever()
