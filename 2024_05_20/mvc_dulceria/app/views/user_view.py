def render_users_list(users):

    return [
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "roles": user.roles
        }
        for user in users
    ]


def render_user_detail(user):
   
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "roles": user.roles
    }