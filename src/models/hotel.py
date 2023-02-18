import json
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from src.functions import has_numbers, is_valid_email, is_valid_url
from .pyObjectId import PyObjectId


class Hotel(BaseModel):
    """
    Class for hotel schema given a basemodel object
    @param {Basemodel}: Basemodel
    """
    id: Optional[PyObjectId] = Field(None, alias="_id")
    name: str
    city: str
    address: str
    contact_email: str
    image_url: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def to_bson_object(self):
        """
        Turn class attributes to a bson object
        returns: DictStrAny
        """
        data = self.dict(by_alias=True, exclude_none=True)
        return data

    def to_json_object(self):
        """
        Turn class attributes to an encoded json object
        returns: string
        """
        return json.dumps(self.__dict__, default=str)

    def validate_fields(self):
        """
        Check if values are correct
        returns: string[]
        """
        errors = []
        if has_numbers(self.name):
            errors.append('Name field cannot have numbers')
        if has_numbers(self.city):
            errors.append('City field cannot have numbers')
        if not is_valid_email(self.contact_email):
            errors.append('Email field is not a valid email')
        if not is_valid_url(self.image_url):
            errors.append('Image Url field is not a valid url')
        return errors
