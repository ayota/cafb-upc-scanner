import os
import unirest

class upc_food(object):
    
    def __init__(self, upc_code):
        """
        Initialize using API key and ID from your environment variables
        """
        self.upc_code = upc_code
        self.api_key = os.environ.get('NIX_API_KEY')
        self.api_id = os.environ.get('NIX_APP_ID')
        self.get_food_item()
        
    def reset_keys(self, new_key):
        """
        Use to change API key that's not the default
        """
        setattr(self, 'api_key', new_key)
        
    def reset_id(self, new_id):
        """
        Use to change API ID that's not set in the default
        """
        setattr(self, 'api_id', new_id)
    
    def get_food_item(self):
        """
        Pull nutritional information from the Nutrionix API
        """
        response = unirest.get("https://api.nutritionix.com/v1_1/item?upc={upc}&appId={apiID}&appKey={apiKey}".format(
                apiID=self.api_id, apiKey=self.api_key,upc=self.upc_code),
                               headers={"Accept": "application/json"})
        self.food_info = response.body
        return self.food_info
