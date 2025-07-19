class SessionManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance.full_name = ""
            cls._instance.logged_in = False
            cls._instance.role = None
        return cls._instance

    def set_full_name(self, full_name):
        self.full_name = full_name

    def get_full_name(self):
        return self.full_name

    def set_logged_in(self, logged_in):
        self.logged_in = logged_in

    def is_logged_in(self):
        return self.logged_in

    def set_role(self, role):
        self.role = role

    def get_role(self):
        return self.role

session_manager = SessionManager()
