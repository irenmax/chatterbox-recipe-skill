from adapt.intent import IntentBuilder
from chatterbox.skills.core import ChatterboxSkill
from chatterbox.skills.core import intent_handler


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
       self.speak("ok, getting recipe")
       # self.recipe = Recipe("recipe_1.txt")
       sl = self.read_recipe("recipe_1.txt")
       self.speak(sl[1])
       self.stepList = sl
       self.speak("got recipe")
       self.speak(len(self.stepList))


    @intent_handler(IntentBuilder("nextStep").require('nextStep'))
    def handle_next_step(self, message):
        step = self.stepList[self.stepCount]
        self.stepCount = self.stepCount + 1
        self.speak(step)


    def read_recipe(self, file_name):
        with self.file_system.open(file_name, "r") as recipe:
            content = recipe.read()
            content = content.replace("\n", "")
            return filter(None, content.split("- [ ] "))

def create_skill():
    return RecipeSkill()
