from adapt.intent import IntentBuilder
from chatterbox.skills.core import ChatterboxSkill
from chatterbox.skills.core import intent_handler

class Recipe:
  stepCount = 0
  def __init__(self, recipeName):
    recipe = open(recipeName, "r")
    content = recipe.read()
    content = content.replace("\n", "")
    Recipe.stepList = filter(None, content.split("- [ ] "))
    recipe.close()
  
  def getLine(self, index):
    return Recipe.stepList[index]

  def getNextStep(self):
    step = Recipe.stepList[Recipe.stepCount]
    Recipe.stepCount = Recipe.stepCount + 1
    return step



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
