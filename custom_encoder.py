import json
from decimal import Decimal


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj) #Explicit Casting here because decimal is not supported
        return json.JSONEncoder.default(self,obj)