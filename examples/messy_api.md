# API de E-commerce

## Endpoints de Usuarios

GET /users
Obtiene la lista completa de usuarios registrados en el sistema.
Retorna un array con todos los usuarios.

POST /users
Crea un nuevo usuario en el sistema.
Requiere email y password.

GET /users/{id}
Obtiene la información de un usuario específico por su ID.

PUT /users/{id}
Actualiza la información de un usuario existente.

DELETE /users/{id}
Elimina un usuario del sistema.

## Endpoints de Productos

GET /products
Lista todos los productos disponibles.

POST /products
Crea un nuevo producto.
Requiere nombre, precio y descripción.

GET /products/{productId}
Obtiene los detalles de un producto específico.

PUT /products/{productId}
Actualiza la información de un producto.

DELETE /products/{productId}
Elimina un producto del catálogo.

## Endpoints de Pedidos

GET /orders
Lista todos los pedidos realizados.

POST /orders
Crea un nuevo pedido.
Requiere userId y lista de productos.

GET /orders/{orderId}
Obtiene los detalles de un pedido específico.

PATCH /orders/{orderId}/status
Actualiza el estado de un pedido.

DELETE /orders/{orderId}
Cancela un pedido.
