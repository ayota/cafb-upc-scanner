import os
import unirest

class upc_food(object):
    
    def __init__(self, upc_code):
        self.upc_code = upc_code
        self.api_key = os.environ.get('NIX_API_KEY')
        self.api_id = os.environ.get('NIX_APP_ID')
#         self.food_type = food_type
        self.get_food_item()
        
    def reset_keys(self, new_key):
        """
        Change API keys
        """
        setattr(self, 'api_key', new_key)
        
    def reset_id(self, new_id):
        """
        Change API id
        """
        setattr(self, 'api_id', new_id)
    
    def get_food_item(self):
        """
        Get nutritional info from the Nutrionix API or add in new item if not found
        """
        response = unirest.get("https://api.nutritionix.com/v1_1/item?upc={upc}&appId={apiID}&appKey={apiKey}".format(
                apiID=self.api_id, apiKey=self.api_key,upc=self.upc_code),
                               headers={"Accept": "application/json"})
        if response.code != 200:
            while add_question != 'Y' | add_question != 'N':
                add_question = input('Item not found, add new item?[Y/N] ')
            if add_question == 'Y':
                self.add_new_food_item()
            else:
                self.food_info = 'Item not found'
        else:
            self.food_info = response.body
            new_dict_keys = map(lambda x:str(x).replace('nf_',''), self.food_info.keys())
            self.food_info = dict(zip(new_dict_keys,self.food_info.values()))
        return self.food_info
    
    def add_new_food_item(self):
        """
        Add new food item, basic inputs
        """
        name = input('Food Name: ')
        sugar = input('Grams of sugar: ')
        sodium = input('Grams of sodium: ')
        fat = input('Grams of fat: ')
        sat_fat = input('Grams of saturated fat: ')
        trans_fat = input('Grams of transaturated fat: ')
        cholesterol = input('Grams of cholesterol: ')
        fiber = input('Grams of fiber: ')
        carbs = input('Grams of carbs: ')
        key_strings = ['name','sugars','sodium','total_fat','saturated_fat','trans_fatty_acid',
                      'cholesterol','dietary_fiber','total_carbohydrate']
        value_strings = [name, sugar, sodium, fat, sat_fat, trans_fat, cholesterol, fiber, carbs]
        self.food_info = dict(zip(key_strings, value_strings))
        return self.food_info
        
    def convert_dict_to_attributes(self):
        """
        Convert the keys in the dictionary to object attributes
        """
        for key, value in self.food_info:
            setattr(self, key, value)
            
    @property
    def main_ingredient(self):
        """
        Extract main ingredient of the food
        """
        return self.food_info['ingredient_statement'].split(',')[0]
    
    def set_food_info(self, nutrition, value):
        """
        Change the nutrtion value of food
        """
        setattr(self, nutrition, value)
    
