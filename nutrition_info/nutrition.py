import os
import unirest

#This will require a Nutrionix API key and ID, which can be found here: https://developer.nutritionix.com/

class upc_food(object):
    
    def __init__(self, upc_code, api_key, api_id):
        self.upc_code = upc_code
        self.api_key = api_key 
        self.api_id = api_id
#         self.food_type = food_type
        self.run()
        
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
        if response.code == 200:
            self.food_info = response.body
            new_dict_keys = map(lambda x:str(x).replace('nf_',''), self.food_info.keys())
            self.food_info = dict(zip(new_dict_keys,self.food_info.values()))
        else:
            while True: 
                add_question = raw_input('API Error or Item not found, add new item?[Y/N] ')
                if (add_question == 'Y') | (add_question == 'N'):
                    break
            if add_question == 'Y':
                self.add_new_food_item()
            else:
                self.food_info = response.body['error_message']
        return self.food_info

    def add_new_food_item(self):
        """
        Add new food item, basic raw_inputs
        """
        name = raw_input('Food Name: ')
        sugar = raw_input('Grams of sugar: ')
        sodium = raw_input('Grams of sodium: ')
        fat = raw_input('Grams of fat: ')
        sat_fat = raw_input('Grams of saturated fat: ')
        trans_fat = raw_input('Grams of transaturated fat: ')
        cholesterol = raw_input('Grams of cholesterol: ')
        fiber = raw_input('Grams of fiber: ')
        carbs = raw_input('Grams of carbs: ')
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
        pass
        #setattr(self, nutrition, value)
    
    def wellness_logic(self):
        if self.sugars < 12 & self.sodium < 50 & self.fiber > 10:
            self.wellness = 'Healthy!'
        else:
            self.wellness = 'Not healthy!'
        return self.wellness
        
    def run():
        self.get_food_item()
        self.convert_dict_to_attributes()
        self.wellness_logic()
