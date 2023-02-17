"""
This module outlines the contents of all the tables with data 
regarding books in the application's database.
"""

from main.extentions import db

class TableBkMetadata(db.Model):
    """This class outlines the structure of the BkMetadata table
    in the application's database, and the related methods. 

    Args:
        db (object): Tables contains metadata for books.

    Returns:
        Integer, string: Returns data as integers or strings.
    """
    __tablename__ = 'bk_metadata'
    bk_metadata_item_id = db.Column('item_id', db.Integer, primary_key=True)
    bk_metadata_url = db.Column('url', db.String(1000))
    bk_metadata_title = db.Column('title', db.String(255))
    bk_metadata_authors = db.Column('authors', db.String(2000))
    bk_metadata_lang = db.Column('lang', db.String(255))
    bk_metadata_img = db.Column('img', db.String(1000))
    bk_metadata_year = db.Column('year', db.Integer)
    bk_metadata_description = db.Column('description', db.String(65535))

    def object_to_dictionary(self):
        """This method returns contents of the BkMetadata table
        in a dictionary format.

        Returns:
            Dictionary: Returns contents of the BkMetadata table.
        """
        return {
            'item_id': self.bk_metadata_item_id,
            'url': self.bk_metadata_url,
            'title': self.bk_metadata_title,
            'authors': self.bk_metadata_authors,
            'lang': self.bk_metadata_lang,
            'img': self.bk_metadata_img,
            'year': self.bk_metadata_year,
            'description': self.bk_metadata_description,
            }
