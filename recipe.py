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


