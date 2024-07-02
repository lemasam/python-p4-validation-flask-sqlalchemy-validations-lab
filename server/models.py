from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self,key,name):
        if not name:
            raise ValueError("Name field is required.")
        author =db.session.query(Author.id).filter_by(name=name).first()
        if author is not None:
            raise ValueError("Name must be unique.")
        return name 
    
    @validates("phone_number")
    def validate_phone_number(self,key,phone_number):
        valid_length = len(phone_number)==10
        is_number = phone_number.isdigit()
        if valid_length and is_number:
            return phone_number
        else: 
            raise ValueError("Phone number must be 10 digits")
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content', 'summary')
    def validate_length(self, key, string):
        if( key == 'content'):
            if len(string) < 250:
                raise ValueError("Post content must be greater than or equal 250 characters long.")
        if( key == 'summary'):
            if len(string) > 250:
                raise ValueError("Post summary must be less than or equal to 250 characters long.")
        return string
    
    @validates('title')
    def validate_title(self,key,title):
        if not title:
            raise ValueError("Title field is required." )
        clickbait =["Won't Believe","Secret", "Top","Guess"]
        if not any(substring in title for substring in clickbait):
            raise ValueError("No clickbait found")
        return title   
     
    @validates('category')
    def validate_category(self, key, category):
        categories = ["Fiction", "Non-Fiction"]
        if category in categories:
            return category
        else:
            raise ValueError("Category must be Fiction or Non-Fiction.")


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
