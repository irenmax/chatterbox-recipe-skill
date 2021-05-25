from adapt.intent import IntentBuilder
from chatterbox.skills.core import ChatterboxSkill
from chatterbox.skills.core import intent_handler
from mycroft.skills.context import adds_context, removes_context
import requests


class Recipe:
    def __init__(self):
        self.stepList = []
        self.ingredients = []
        self.stepCount = 0
        self.started = False

    # loads recipe via http
    # returns True if recipe was found    
    def loadRecipe(self, recipeName):
        self.stepList = []
        self.ingredients = []
        self.stepCount = 0
        self.started = False

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
        self.started = True
        if len(self.stepList) > 0 and self.stepCount < len(self.stepList):
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
                return self.stepList[self.stepCount - 1]
            else:
                return 'No more steps'
        else:
            return 'This recipe has no steps'

    def getFirstStep(self, resetCounter):
        self.started = True
        if resetCounter:
            self.stepCount = 0
        return self.getNextStep()

    def ingredientsToString(self):
      ingredientString = ""
      if len(self.ingredients) > 0:
        for i in self.ingredients:
          ingredientString = ingredientString + str(i.get("amount")) + " " + i.get("unit") + " " + str(i.get("name")) + ".\n"
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

    #### GET RECIPE ####    

    @intent_handler('get.recipe.for.intent')
    def handle_getRecipe(self, message):
        recipeName = message.data.get('entities', {}).get('name')
        if recipeName is not None:
            self.log.debug(recipeName)
            if recipeName == 'it':
                self.speak('blabla')
            else:
                self.speak('Okay, i am searching the recipe for ' + recipeName)
                foundRecipe = self.recipe.loadRecipe(recipeName)
                if foundRecipe:
                    self.speak('I have found a recipe for ' + recipeName)
                else:
                    self.speak('I could not find a recipe for ' + recipeName)
        else:
            self.speak('I could not understand what recipe you want.')
            
    #### INSTRUCTIONS ####

    @intent_handler(IntentBuilder('startInstructions').require('startInstructions'))
    @adds_context('ListIntredients')
    def handle_startInstructions(self, message):
        self.speak("Would you like to hear the ingredients?", expect_response=True)


    @intent_handler(IntentBuilder('YesListIngredients').require('yesKeyword').require('ListIngredients').build())
    @removes_context('ListIngredients')
    @adds_context('StartFromBeginning')
    def handle_listIngredients(self, message):
        self.speak(self.recipe.ingredientsToString())
        if self.recipe.started:
            self.speak("Do you want to start the isntructions from the beginning?", expect_response=True)
        else:
            self.speak("Here are the instructions.")
            self.speak(self.recipe.getNextStep())

    @intent_handler(IntentBuilder('NoListIngredients').require('noKeyword').require('ListIngredients').build())
    @removes_context('ListIngredients')
    @adds_context('StartFromBeginning')
    def handle_doNotListIngredients(self, message):
        self.speak("Okay, i will just tell you the steps.")
        if self.recipe.started:
            self.speak("Do you want to start from the beginning?", expect_response=True)
        else:
            self.speak(self.recipe.getNextStep())


    @intent_handler(IntentBuilder('YesFromBeginningIntent').require('yesKeyword').require('StartFromBeginning').build())
    @removes_context('StartFromBeginning')
    def handle_startFromBeginning(self, message):
        self.speak('Okay, i start from the beginning.')
        self.speak(self.recipe.getFirstStep(resetCounter=True))

    @intent_handler(IntentBuilder('NoFromBeginningIntent').require('noKeyword').require('StartFromBeginning').build())
    def handle_doNotStartFromBeginning(self, message):
        self.speak('Okay, here is the next step.')
        self.speak(self.recipe.getNextStep())       
       
    @intent_handler(IntentBuilder('nextStep').require('nextStep'))
    def handle_nextStep(self, message):
        self.speak(self.recipe.getNextStep())
    
    @intent_handler(IntentBuilder('repeatStep').require('repeatStep'))
    def handle_repeatStep(self, message):
        self.speak(self.recipe.repeatStep())


    #### INGREDIENTS ####

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