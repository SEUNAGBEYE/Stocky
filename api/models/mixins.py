"""Module for generic model operations mixin."""

from .config import db

class ModelMixin:
    """Mixin class with generic model operations."""

    def save(self):
        """
        Save a model instance
        """
        db.session.add(self)
        db.session.commit()
        return self

    def update_(self, **kwargs):
        """
        Updates a record

        Args:
            kwargs (dict): Key-value pair of the attributes to update
        
        Returns:
            (dict) The updated record
        """
        for field, value in kwargs.items():
            setattr(self, field, value)
        db.session.commit()

    @classmethod
    def get(cls, id):
        """
        Gets a record by id

        Args:
            id (int): Unique identifier for the recod
        
        Returns:
            (dict) The found record
        """
        
        return cls.query.get(id)

    @classmethod
    def get_or_404(cls, id):
        """
        Gets a record or return 404

        Args:
            id (int): Unique identifier for the recod
        
        Returns:
            (dict) The found record
        
        Raises:
            (exception) Not found exeption if the record does not exist
        """
        
        record = cls.get(id)

        if not record:
            raise ValidationError(
                {
                    'message':
                    f'{re.sub(r"(?<=[a-z])[A-Z]+",lambda x: f" {x.group(0).lower()}" , cls.__name__)} not found'  # noqa
                },
                404)

        return record

    def delete(self):
        """
        Soft delete a model instance.
        """
        pass

    @classmethod
    def count(cls):
        """
        Returns the number of records that satify a query
        """
        
        return cls.query.count()

    @classmethod
    def find_or_create(cls, data, **kwargs):
        """
        Finds a model instance or creates it

        Args:
            data (dict): details of the record to be created
        
        Returns:
            (dict) The found record or newly created record
        """
        
        instance = cls.query.filter_by(**kwargs).first()
        if not instance:
            instance = cls(**data).save()
        return instance

    @classmethod
    def bulk_create(cls, objects):
        """
        Saves a list of records (dict) to database

        Args:
            objects (list): List of records to be saved to database

        Returns:
            (list): A list of the newly created records
        """
        
        resource_list = [cls(**item) for item in objects]
        db.session.add_all(resource_list)
        db.session.commit()

        return resource_list

