from adapt.intent import IntentBuilder
from chatterbox import ChatterboxSkill, intent_handler

class RecipeSkill(ChatterboxSkill):
  def __init__(self):
    super().__init__()
    self.already_said_hello = False
    self.be_friendly = True
  
  @intent_handler('hear_this.intent')
  def handle_hello_intent(self, message):
    self.speak_dialog('say_this.dialog')

  def stop(self):
    pass

  def create_skill():
    return RecipeSkill()