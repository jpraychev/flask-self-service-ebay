from werkzeug.security import generate_password_hash

users = {
    "test": generate_password_hash("test"),
}