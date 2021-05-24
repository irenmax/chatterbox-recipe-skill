from adapt.intent import IntentBuilder
from chatterbox.skills.core import ChatterboxSkill
from chatterbox.skills.core import intent_handler
import requests


class Recipe:
    def __init__(self):
        self.stepList = []
        self.stepCount = 0

    # loads recipe via http
    # returns True if recipe was found    
    def loadRecipe(self, recipeName):
        self.stepList = []
        self.stepCount = 0
        response = requests.get("http://192.168.0.80:8989/" + recipeName + ".md")
        if response.status_code is 200:
            content = str(response.text)
            content = content.replace("\n", "")
            self.stepList = list(filter(None, content.split("- [ ] ")))
            return True
        else:
            return False
    
    def getNextStep(self):
        if self.stepCount < len(self.stepList):
            step = self.stepList[self.stepCount]
            self.stepCount = self.stepCount + 1
            return step
        else:
            return 'No more steps'

        


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
            self.speak('Okay, i am searching the reicipe for ' + recipeName)
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

def create_skill():
    return RecipeSkill()