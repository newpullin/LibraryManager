from sqlalchemy import text

class StatusDao:
	def __init__(self, database):
		self.db = database
	def get_books(self):
		row = self.db.execute("SELECT * from book;")
		books = row.fetchall()
		return [{'ISBN': book['ISBN'],
		'title': book['title'],
		'writers':book['writers'],
		'translator':book['translator'],
		'publisher':book['publisher'],
		'published_at': book['published_at'],
		'kdc ': book['kdc'],
		'img_url' : book['img_url']
		} for book in books]
	def get_libraries(self):
		row = self.db.execute("SELECT * from libraries;")
		libss = row.fetchall()
		return [{'lib_id': library['id'], 'lib_name': library['name'], 'tel': library['tel'],'location': library['location']} for library in libss]
	def get_status(self, user_id):
		user_status = self.db.execute(text("""
			SELECT 
                t.user_id,
                t.lib_id,
                t.ISBN,
                t.landing_at,
                t.landing_status
            FROM user_status t
            WHERE t.user_id = :user_id;
        """), {
            'user_id' : user_id 
        }).fetchall()

		return [{
            'user_id' : status['user_id'],
            'lib_id'   : status['lib_id'],
            'ISBN' : status['ISBN'],
            'landing_at' : status['landing_at'],
            'landing_status' : status['landing_status']
        } for status in user_status]
