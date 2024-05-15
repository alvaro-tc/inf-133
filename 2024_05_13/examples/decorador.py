from functools import wraps

# Define un decorador que imprime un mensaje antes
# y despues de llamar a la funcion decorada
# Usando wraps para mantener los metadatos de la funcion original

def my_decorator(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        print("Antes de llamar a la funcion")
        result = func(*args,**kwargs)
        print("Despues de llamar a la funcion")
        return result   
    return wrapper


#Aplica el decorador a una funcion
@my_decorator
def greet(name):
    return name

#Llama a la funcion decorada


#Accede a los metadatos de la funcion original
print(greet.__name__)
#Output: greet
print(greet.__doc__)
#Output: Funcion para saludar a alguien