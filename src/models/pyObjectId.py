from bson import ObjectId


class PyObjectId(ObjectId):
    """
    Class to make possible to type objectId from mongoDB documents into pydantic schema 
    @param: {ObjectID}: ObjectID
    """
    @classmethod
    def __get_validators__(cls):
        """
        Execute a validation of the current object
        """
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """
        Generate an ObjectID object with the field value of PyObjectId
        """
        return ObjectId(str(v))
