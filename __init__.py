from adapt.intent import IntentBuilder
from chatterbox.skills.core import ChatterboxSkill
from chatterbox.skills.core import intent_handler
import requests


def loadRecipe(stepCounter, stepList, recipeName):
    stepCounter = 0
    response = requests.get('http://1e2ba836c4e1.ngrok.io/recipe_1.txt')
    content = response.content
    content = content.replace("\n", "")
    stepList = filter(None, content.split("- [ ] "))
    return stepCounter, stepList
  
def getNextStep(stepCounter, stepList):
    if stepCounter < len(stepList):
        step = stepList[stepCounter]
        stepCounter = stepCounter + 1
        return step
    else:
        return 'No more steps'



class RecipeSkill(ChatterboxSkill):
    def __init__(self):
        super().__init__()
        self.stepCounter = 0
        self.stepList = []

    
    @intent_handler(IntentBuilder('helloWorld').require('hello'))
    def handle_intent_helloWorld(self, message):
        self.speak('hello world')

    @intent_handler(IntentBuilder('getRecipe').require('getRecipe'))
    def handle_getRecipe(self, message):
        self.stepCounter, self.stepList = loadRecipe(self.stepCounter, self.stepList, 'recipe1')
       
    @intent_handler(IntentBuilder('nextStep').require('nextStep'))
    def handle_nextStep(self, message):
        self.speak('Okay')
        step = getNextStep(self.stepCounter, self.stepList)
        self.speak(step)

def create_skill():
    return RecipeSkill()