from application import db
from application.models import Pictures, Tags

db.create_all()

print("Database created.")
