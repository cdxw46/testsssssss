from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if "/auth/register" in self.path:
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode()
            
            print(f"\n{'='*60}")
            print("REGISTRATION RECEIVED:")
            print(f"Body: {body}")
            print(f"{'='*60}\n")
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            resp = json.dumps({"success": True, "message": "Registered", "flag": "HTB{test_flag_12345}"})
            self.wfile.write(resp.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress default logs

print("Servidor falso iniciado en puerto 3000")
print("Configurar la app Android para conectarse a este servidor")
HTTPServer(('0.0.0.0', 3000), Handler).serve_forever()
