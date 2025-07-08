from config import supabase

def login_user(email, password):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        if res.user:
            return {
                "user_id": res.user.id,
                "email": res.user.email,
                "role": res.user.user_metadata.get("role", None)
            }
    except Exception as e:
        return None
