from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

productos = {}

class Producto():
    def __init__(self) :
        self.descripcion = None
        self.cantidad = None
        self.precio = None
    def setProducto(self,descripcion,cantidad,precio):
        self.cantidad= cantidad
        self.descripcion= descripcion
        self.precio= precio
        
class ProductoService():
    
    def leerProductos(self):
        return {id: producto.__dict__ for id, producto in productos.items()}
    def crearProductos(self,post_data):
        cantidad = post_data.get('cantidad',None)
        descripcion = post_data.get('descripcion',None)
        precio = post_data.get('precio',None)
        producto = Producto()
        producto.setProducto(cantidad,descripcion,precio)
        
        if productos:
            new_id = max(productos.keys())+1
        else:
            new_id= 1
        productos[new_id]=producto
        return producto.__dict__
    def eliminarProducto(self,id_producto):
        del productos[id_producto]
        return None
    def modificarProducto(self,id_producto,post_data):
        cantidad = post_data.get('cantidad',None)
        descripcion = post_data.get('descripcion',None)
        precio = post_data.get('precio',None)
        producto = Producto()
        producto.setProducto(cantidad,descripcion,precio)
        if id_producto in productos:
            producto = productos[id_producto]
            if cantidad:
                producto.cantidad= cantidad
            if descripcion:
                producto.descripcion= descripcion
            if precio:
                producto.precio= precio
        else:
            return None
    def buscar_Precio(self, post_data):
        precio = post_data.get('precio',None)
        return {key: producto.__dict__ for key, producto in productos.items() if getattr(producto, "precio") == precio}


class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))


class ProductosHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controller = ProductoService()
        super().__init__(*args, **kwargs)
        
    def do_POST(self):
        post_data = HTTPDataHandler.handle_reader(self)
        if self.path == '/productos':
            data=self.controller.crearProductos(post_data)
            HTTPDataHandler.handle_response(self,201,data)
        else:
            HTTPDataHandler.handle_response(self,404,{"Error":"Ruta no existente"})
    def do_GET(self):
        if self.path == "/productos":
            response_data = self.controller.leerProductos()
            HTTPDataHandler.handle_response(self, 200, response_data)
        
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})
    def do_PUT(self):
        post_data = HTTPDataHandler.handle_reader(self)
        if self.path.startswith("/productos/"):
            id = int(self.path.split("/")[-1])
            response_data=ProductoService.modificarProducto(id,post_data)
            if response_data:
                HTTPDataHandler.handle_response(self,200,response_data)
            else:
                HTTPDataHandler.handle_response(self,404,{"Message":"Producto no existente"})
        else:
            HTTPDataHandler.handle_response(self,404,{"Error":"Ruta no existente"})
    def do_DELETE(self):
        post_data = HTTPDataHandler.handle_reader(self)
        if self.path.startswith("/productos/"):
            id = int(self.path.split("/")[-1])
            response_data=ProductoService.eliminarProducto(id)
            if response_data:
                HTTPDataHandler.handle_response(self,200,{"Message":"Producto eliminado"})
            else:
                HTTPDataHandler.handle_response(self,404,{"Message":"Producto no existente"})
        else:
            HTTPDataHandler.handle_response(self,404,{"Error":"Ruta no existente"})


def run(server_class=HTTPServer, handler_class=ProductosHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor HTTP en puerto http://localhost:{port}/")
    httpd.serve_forever()


if __name__ == "__main__":
    run()

    
