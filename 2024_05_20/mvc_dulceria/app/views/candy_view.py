def render_candy_list(candies):

    return [
        {
            "id": candy.id,
            "marca": candy.marca,
            "peso": candy.peso,
            "sabor": candy.sabor,
            "origen": candy.origen
        }
        for candy in candies
    ]


def render_candy_detail(candy):
   
    return {
        "id": candy.id,
        "marca": candy.marca,
        "peso": candy.peso,
        "sabor": candy.sabor,
        "origen": candy.origen
    }