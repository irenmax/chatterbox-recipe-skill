from adapt.intent import IntentBuilder
from chatterbox.skills.core import ChatterboxSkill
from chatterbox.skills.core import intent_handler


class HelloWorldSkill(ChatterboxSkill):

    @intent_handler(IntentBuilder("helloWorld").
                    require('hello').require('world'))
    def handle_intent_name2Intent(self, message):
        self.speak('hello world')


def create_skill():
    return HelloWorldSkill()