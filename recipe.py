import requests

class Recipe:
  def __init__(self):
    self.stepList = []
    self.stepCount = 0
    response = requests.get('http://1e2ba836c4e1.ngrok.io/recipe_1.txt')
    content = response.content
    content = content.replace("\n", "")
    self.stepList = filter(None, content.split("- [ ] "))
  
  def getLine(self, index):
    return self.stepList[index]

  def getNextStep(self):
    if self.stepCount < len(self.stepList):
      step = self.stepList[self.stepCount]
      self.stepCount = self.stepCount + 1
      return step
    else:
      return 'No more steps'


