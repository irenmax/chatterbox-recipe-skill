from adapt.intent import IntentBuilder
from chatterbox.skills.core import ChatterboxSkill
from chatterbox.skills.core import intent_handler
from recipe import Recipe

class RecipeSkill(ChatterboxSkill):
    def __init__(self):
        super().__init__()

    
    @intent_handler(IntentBuilder('helloWorld').require('hello'))
    def handle_intent_helloWorld(self, message):
        self.speak('hello world')

    @intent_handler(IntentBuilder('getRecipe').require('getRecipe'))
    def handle_getRecipe(self, message):
        self.recipe1 = Recipe()
        self.speak('Okay')
       
    @intent_handler(IntentBuilder('nextStep').require('nextStep'))
    def handle_nextStep(self, message):
        self.speak('Okay')
        step = self.recipe1.getNextStep()
        self.speak(step)

def create_skill():
    return RecipeSkill()