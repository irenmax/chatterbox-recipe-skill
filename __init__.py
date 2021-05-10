from adapt.intent import IntentBuilder
from chatterbox.skills.core import ChatterboxSkill
from chatterbox.skills.core import intent_handler


class RecipeSkill(ChatterboxSkill):
    
    @intent_handler(IntentBuilder("helloWorld").
                    require('hello'))
    def handle_intent_name2Intent(self, message):
        self.speak('hello world')

    @intent_handler(IntentBuilder("getRecipe").require('getRecipe'))
    def handle_getRecipe(self, message):
       # self.recipe = Recipe("recipe_1.txt")
       with self.file_system.open("recipe_1.txt", "w") as recipe:
           content = recipe.read()
           content = content.replace("\n", "")
           self.stepList = filter(None, content.split("- [ ] "))
           self.stepCount = 0
           recipe.close()

    @intent_handler(IntentBuilder("nextStep").require('nextStep'))
    def handle_next_step(self, message):
        step = self.stepList[self.stepCount]
        self.stepCount = self.stepCount + 1
        self.speak(step)

def create_skill():
    return RecipeSkill()
