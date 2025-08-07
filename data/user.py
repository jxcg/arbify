import requests

class User:
    def __init__(self):
        self.ip = self.get_user_ip()
        self.request_count = 0
        self.session_data = {}
        # Add other attributes as needed, e.g.:
        # self.last_request_time = None

    def get_user_ip(self):
        try:
            return requests.get('https://api.ipify.org').text
        except Exception:
            return "Unknown"



    def get_ip(self):
        return self.ip



    def increment_requests(self):
        self.request_count += 1



    def set_session_data(self, key, value):
        self.session_data[key] = value



    def get_session_data(self, key, default=None):
        return self.session_data.get(key, default)



    def __repr__(self):
        return f"<User IP={self.ip} requests={self.request_count}>"