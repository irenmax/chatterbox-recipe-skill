from adapt.intent import IntentBuilder
from chatterbox.skills.core import ChatterboxSkill
from chatterbox.skills.core import intent_handler
import requests


def loadRecipe(stepCounter, stepList, recipeName):
    stepCounter = 0
    file = str(requests.get("http://3d6feb466bd8.ngrok.io/recipe_1.txt").text)
    content = file.replace("\n", "")
    stepList = list(filter(None, content.split("- [ ] ")))
    return stepCounter, stepList
  
def getNextStep(stepCounter, stepList):
    if stepCounter < len(stepList):
        step = stepList[stepCounter]
        stepCounter = stepCounter + 1
        return step
    else:
        return 'No more steps'


class Recipe:
    def __init__(self):
        self.stepList = []
        self.stepCount = 0
        
    def loadRecipe(self, recipeName):
        self.stepList = []
        self.stepCount = 0
        response = str(requests.get("http://3d6feb466bd8.ngrok.io/recipe_1.txt").text)
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
        #self.stepCount = 0
        #self.stepList = []
        self.recipe = Recipe()

    
    @intent_handler(IntentBuilder('helloWorld').require('hello'))
    def handle_intent_helloWorld(self, message):
        self.speak('hello world')

    @intent_handler(IntentBuilder('getRecipe').require('getRecipe'))
    def handle_getRecipe(self, message):
        self.speak('Okay')
        self.recipe.loadRecipe('recipe1')
        self.speak('I have found the recipe')
 #       self.speak('Okay')
 #       self.stepCount, self.stepList = loadRecipe(self.stepCount, self.stepList, 'recipe1')
 #       self.speak('Done')
       
    @intent_handler(IntentBuilder('nextStep').require('nextStep'))
    def handle_nextStep(self, message):
        self.speak(self.recipe.getNextStep())
  #      self.speak('Okay')
  #      step = getNextStep(self.stepCount, self.stepList)
  #      self.speak(step)


def create_skill():
    return RecipeSkill()