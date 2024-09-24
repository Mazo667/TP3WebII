import logging

class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Print the request details to the console
        print(f"Método de solicitud: {request.method}, Ruta de solicitud: {request.path}")

        # Call the next middleware or view
        response = self.get_response(request)

        # Print the response status code to the console
        print(f"Código de estado de la respuesta: {response.status_code}")

        return response