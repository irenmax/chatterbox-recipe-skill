from adapt.intent import IntentBuilder
from chatterbox.skills.core import ChatterboxSkill
from chatterbox.skills.core import intent_handler


class HelloWorldSkill(ChatterboxSkill):

    @intent_handler(IntentBuilder("helloWorld").
                    require('hello'))
    def handle_intent_name2Intent(self, message):
        self.speak('hello world')

    @intent_handler(IntentBuilder("nextLine").require('nextline'))
    def handle_next_line(self, message):
      self.speak('This is the next line')

def create_skill():
    return HelloWorldSkill()