from adapt.intent import IntentBuilder
from chatterbox.skills.core import ChatterboxSkill
from chatterbox.skills.core import intent_handler
import urllib3


class RecipeSkill(ChatterboxSkill):


    def __init__(self):
        super().__init__()
        self.stepCount = 0
        self.stepList = []
    
    @intent_handler(IntentBuilder("helloWorld").
                    require('hello'))
    def handle_intent_name2Intent(self, message):
        self.speak('hello world')

    @intent_handler(IntentBuilder("getRecipe").require('getRecipe'))
    def handle_getRecipe(self, message):
       http = urllib3.PoolManager()
       response = http.request('GET', 'http://1e2ba836c4e1.ngrok.io/recipe_1.txt')
       status = response.status
       content = response.data
       self.speak(status)
       self.speak(content)


    @intent_handler(IntentBuilder("nextStep").require('nextStep'))
    def handle_next_step(self, message):
        step = self.stepList[self.stepCount]
        self.stepCount = self.stepCount + 1
        self.speak(step)



def create_skill():
    return RecipeSkill()
