"""Module for generic model operations mixin."""

class ModelMixin:
    """Mixin class with generic model operations."""

    def save(self):
        """
        Save a model instance
        """
        pass

    def update_(self, **kwargs):
        """
        Updates a record

        Args:
            kwargs (dict): Key-value pair of the attributes to update
        
        Returns:
            (dict) The updated record
        """
        pass

    @classmethod
    def get(cls, id):
        """
        Gets a record by id

        Args:
            id (int): Unique identifier for the recod
        
        Returns:
            (dict) The found record
        """
        pass

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
        pass

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
        pass

    @classmethod
    def find_or_create(cls, data, **kwargs):
        """
        Finds a model instance or creates it

        Args:
            data (dict): details of the record to be created
        
        Returns:
            (dict) The found record or newly created record
        """
        pass

    @classmethod
    def bulk_create(cls, objects):
        """
        Saves a list of records (dict) to database

        Args:
            objects (list): List of records to be saved to database

        Returns:
            (list): A list of the newly created records
        """
        pass

