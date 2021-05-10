from adapt.intent import IntentBuilder
from chatterbox.skills.core import ChatterboxSkill
from chatterbox.skills.core import intent_handler
from recipe import Recipe



class RecipeSkill(ChatterboxSkill):
    
    @intent_handler(IntentBuilder("helloWorld").
                    require('hello'))
    def handle_intent_name2Intent(self, message):
        self.speak('hello world')

    @intent_handler(IntentBuilder("getRecipe").require('getRecipe'))
    def handle_getRecipe(self, message):
        self.recipe = Recipe("recipe_1.txt")

    @intent_handler(IntentBuilder("nextStep").require('nextStep'))
    def handle_next_step(self, message):
        self.speak(self.recipe.getNextStep())

def create_skill():
    return RecipeSkill()
