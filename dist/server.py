import http.server
import socketserver

PORT = 8811  # 选择一个合适的端口

# 为了加载 index.html，我们需要指定一个处理程序
Handler = http.server.SimpleHTTPRequestHandler

# 启动服务器
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("在端口", PORT, "上启动服务器...")
    # 服务器将一直运行，直到手动中断
    httpd.serve_forever()
