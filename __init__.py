from adapt.intent import IntentBuilder
from chatterbox.skills.core import ChatterboxSkill
from chatterbox.skills.core import intent_handler
import requests


class Recipe:
    def __init__(self):
        self.stepList = []
        self.stepCount = 0
        
    def loadRecipe(self, recipeName):
        self.stepList = []
        self.stepCount = 0
        response = str(requests.get("http://192.168.0.80:8989/recipe_1.md").text)
        content = response.replace("\n", "")
        self.stepList = list(filter(None, content.split("- [ ] ")))
    
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
        self.log.debug(message)
        self.log.debug(message.data)
        recipeName = message.data.entities.get('name')
        
        self.speak(str(recipeName), wait=True)
      #  self.speak('Okay')
      #  self.recipe.loadRecipe('recipe1')
      #  self.speak('I have found the recipe')
       
    @intent_handler(IntentBuilder('nextStep').require('nextStep'))
    def handle_nextStep(self, message):
        self.speak(self.recipe.getNextStep())

def create_skill():
    return RecipeSkill()