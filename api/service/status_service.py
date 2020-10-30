
class StatusService:
    def __init__(self, status_dao):      
        self.status_dao = status_dao

    def get_status(self, user_id):
        return self.status_dao.get_status(user_id)
    
    def get_libraries(self):
        return self.status_dao.get_libraries()      
    def get_books(self):
        return self.status_dao.get_books()

