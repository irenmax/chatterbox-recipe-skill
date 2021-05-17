from adapt.intent import IntentBuilder
from chatterbox.skills.core import ChatterboxSkill
from chatterbox.skills.core import intent_handler
import requests


def loadRecipe(stepCounter, stepList, recipeName):
    stepCounter = 0
    file = str(requests.get("http://3d6feb466bd8.ngrok.io/recipe_1.txt").text), wait=True)
    content = file.replace("\n", "")
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
        self.stepCount = 0
        self.stepList = []

    
    @intent_handler(IntentBuilder('helloWorld').require('hello'))
    def handle_intent_helloWorld(self, message):
        self.speak('hello world')

    @intent_handler(IntentBuilder('getRecipe').require('getRecipe'))
    def handle_getRecipe(self, message):
        self.speak('Okay')
        self.stepCount, self.stepList = loadRecipe(self.stepCount, self.stepList, 'recipe1')
        self.speak('Done')
       
    @intent_handler(IntentBuilder('nextStep').require('nextStep'))
    def handle_nextStep(self, message):
        self.speak('Okay')
        step = getNextStep(self.stepCount, self.stepList)
        self.speak(step)

def create_skill():
    return RecipeSkill()