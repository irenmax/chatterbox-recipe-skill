from adapt.intent import IntentBuilder
from chatterbox.skills.core import ChatterboxSkill
from chatterbox.skills.core import intent_handler
import requests

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
        #response = requests.get('http://1e2ba836c4e1.ngrok.io/recipe_1.txt')
        #self.speak(response.status_code)
        #self.speak(response.content)
        self.stepList =["One", "Two", "Three"]
        self.speak("OK")
       
    @intent_handler(IntentBuilder('nextStep').require('nextStep'))
    def handle_nextStep(self, message):
        step = self.stepList[self.stepCount]
        self.stepCount = self.stepCount + 1
        self.speak(step)

def create_skill():
    return RecipeSkill()