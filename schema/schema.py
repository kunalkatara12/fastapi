def individual_serial(user)->dict:
    return{
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "full_name": user["full_name"],
        "password": user["password"]
    }
    
def many_serial(users)->list:
    return [individual_serial(user) for user in users]    