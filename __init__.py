from adapt.intent import IntentBuilder
from chatterbox.skills.core import ChatterboxSkill
from chatterbox.skills.core import intent_handler
import urllib


class RecipeSkill(ChatterboxSkill):


    def read_recipe(self, file_name):
        recipe = urllib.urlopen("http://b55ecb909419.ngrok.io/recipe_1.txt")
        content = recipe.read()
        content = content.replace("\n", "")
        return filter(None, content.split("- [ ] "))

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
       self.speak("ok, getting recipe")
       # self.recipe = Recipe("recipe_1.txt")
       sl = self.read_recipe("recipe_1.txt")
       self.stepList = sl
       self.speak("got recipe")
       self.speak(len(self.stepList))


    @intent_handler(IntentBuilder("nextStep").require('nextStep'))
    def handle_next_step(self, message):
        step = self.stepList[self.stepCount]
        self.stepCount = self.stepCount + 1
        self.speak(step)



def create_skill():
    return RecipeSkill()
