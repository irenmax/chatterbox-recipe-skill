from adapt.intent import IntentBuilder
from chatterbox.skills.core import ChatterboxSkill
from chatterbox.skills.core import intent_handler
import requests


class Recipe:
    def __init__(self):
        self.stepList = []
        self.ingredients = []
        self.stepCount = 0

    # loads recipe via http
    # returns True if recipe was found    
    def loadRecipe(self, recipeName):
        self.stepList = []
        self.ingredients = []
        self.stepCount = 0

        # replaces spaces in string
        recipeName = recipeName.lower().replace(" ", "_")
    

        response = requests.get("http://192.168.0.80:8989/" + recipeName + ".json")
        if response.status_code == 200:
            # extract ingredients
            ingredients = response.json().get("ingredients")
            for i in ingredients:
              self.ingredients.append(i)

            # extract method
            self.stepList = response.json().get("method")
            return True
        else:
            return False        
    
    def getNextStep(self):
        if len(self.stepList > 0):
            if self.stepCount < len(self.stepList):   
                step = self.stepList[self.stepCount]
                self.stepCount = self.stepCount + 1
                return step
            else:
                return 'No more steps'
        else:
            return 'This recipe has no steps'
        
    def repeatStep(self):
        if len(self.stepList) > 0:
            if self.stepCount < len(self.stepList):
                return self.stepList[self.stepCount]
            else:
                return 'No more steps'
        else:
            return 'This recipe has no steps'

    def ingredientsToString(self):
      ingredientString = ""
      if len(self.ingredients) > 0:
        for i in self.ingredients:
          ingredientString = ingredientString + i.get("name") + "," + str(i.get("amount")) + "."
        return ingredientString
      else:
        return "This recipe has no ingredients"

    def getAmount(self, ingredientName):
      if len(self.ingredients) > 0:
        for i in self.ingredients:
          if ingredientName.lower() in i.get('name').lower():
            return str(i.get("amount")) + " " +  i.get('name')
        
        return "Could not find ingredient"
      else:
        return "This recipe has no ingredients"

        


class RecipeSkill(ChatterboxSkill):
    def __init__(self):
        super().__init__()
        self.recipe = Recipe()
    
    @intent_handler(IntentBuilder('helloWorld').require('hello'))
    def handle_intent_helloWorld(self, message):
        self.speak('hello world')

    @intent_handler('get.recipe.for.intent')
    def handle_getRecipe(self, message):
        recipeName = message.data.get('entities', {}).get('name')
        if recipeName is not None:
            self.speak('Okay, i am searching the recipe for ' + recipeName)
            foundRecipe = self.recipe.loadRecipe(recipeName)
            if foundRecipe:
                self.speak('I have found a recipe for ' + recipeName)
            else:
                self.speak('I could not find a recipe for ' + recipeName)
        else:
            self.speak('I could not understand what recipe you want.')
            
       
    @intent_handler(IntentBuilder('nextStep').require('nextStep'))
    def handle_nextStep(self, message):
        self.speak(self.recipe.getNextStep())
    
    @intent_handler(IntentBuilder('repeatStep').require('repeatStep'))
    def handle_repeatStep(self, message):
        self.speak(self.recipe.repeatStep())

    @intent_handler(IntentBuilder('getIngredients').require('getIngredients'))
    def handle_getIngredients(self, message):
        self.speak(self.recipe.ingredientsToString())
    
    @intent_handler('get.amount.of.ingredient.intent')
    def handle_getAmountOfIngredient(self, message):
        ingredient = message.data.get('entities', {}).get('ingredient')
        if ingredient is not None:
            self.speak(self.recipe.getAmount(ingredient))
        else:
            self.speak("I could not understand the ingredient.")

        

def create_skill():
    return RecipeSkill()