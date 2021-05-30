from adapt.intent import IntentBuilder
from chatterbox.skills.core import ChatterboxSkill
from chatterbox.skills.core import intent_handler
from mycroft.skills.context import adds_context, removes_context
import requests


class Recipe:
    def __init__(self):
        self.loaded = False
        self.stepList = []
        self.ingredients = []
        self.stepCount = 0
        self = None

    # loads recipe via http
    # returns True if recipe was found    
    def loadRecipe(self, recipeName):
        self.stepList = []
        self.ingredients = []
        self.stepCount = 0

        # replaces spaces in string
        recipeName = recipeName.lower().replace(' ', '_')
    

        response = requests.get('http://192.168.0.80:8989/' + recipeName + '.json')
        if response.status_code == 200:
            # extract ingredients
            ingredients = response.json().get('ingredients')
            for i in ingredients:
              self.ingredients.append(i)

            # extract method
            self.stepList = response.json().get('method')
            self.loaded = True
            return True
        else:
            return False        
    
    def getNextStep(self):
        if self.loaded:
            if len(self.stepList) > 0:
                if self.stepCount < len(self.stepList):   
                    step = self.stepList[self.stepCount]
                    self.stepCount = self.stepCount + 1
                    return step
                else:
                    return 'There are no more steps, enjoy your meal!'
            else:
                return 'This recipe has no steps. Just mix it all together.'
        else:
            return 'You havent told me yet, what you want to cook.'
        
    def repeatStep(self):
        if self.loaded:
            if len(self.stepList) > 0:
                if self.stepCount < len(self.stepList):
                    return self.stepList[self.stepCount - 1]
                else:
                    return 'No more steps'
            else:
                return 'This recipe has no steps'
        else:
            return 'You havent told me yet, what you want to cook.'

    def getFirstStep(self, resetCounter):
        if self.loaded:
            if resetCounter:
                self.stepCount = 0
            return self.getNextStep()
        else:
            return 'You havent told me yet, what you want to cook.'

    def ingredientsToString(self):
        if self.loaded:
            if len(self.ingredients) > 0:
                ingredientString = 'You need '
                for i in self.ingredients:
                    ingredientString = ingredientString + '{amount} {unit} of {name}.\n'.format(
                        amount=str(i.get('amount')),
                        unit = i.get('unit'),
                        name = i.get('name')
                        )
                return ingredientString
            else:
                return 'This recipe has no ingredients'
        else:
            return 'You havent told me yet, what you want to cook.'

    def getAmount(self, ingredientName):
        if self.loaded:
            if len(self.ingredients) > 0:
                for i in self.ingredients:
                    if ingredientName.lower() in i.get('name').lower():
                        return 'You need {amount} {unit} of {name}.'.format(
                            amount=str(i.get('amount')),
                            unit=i.get('unit'),
                            name=i.get('name')
                        )
                
                return 'You do not need ' + ingredientName + ' for this recipe.'
            else:
                return 'This recipe has no ingredients.'
        else:
            return 'You havent told me yet, what you want to cook.'
 

        


class RecipeSkill(ChatterboxSkill):
    def __init__(self):
        super().__init__()
        self.recipe = Recipe()
    
    @intent_handler(IntentBuilder('helloWorld').require('hello'))
    def handle_intent_helloWorld(self, message):
        self.speak('hello world')

    #### GET RECIPE ####    

    # user asks for a recipe
    # tells user if a recipe was found for the given dish, asks if it should read the recipe
    # if user asks for 'it' the instructions are read, assuming that user refers to previous wished dish
    @intent_handler('get.recipe.for.intent')
    @adds_context('StartRecipeContext')
    def handle_getRecipe(self, message):
        recipeName = message.data.get('entities', {}).get('name')
        if recipeName is not None:
            self.log.debug(recipeName)
            if recipeName == 'it':
                self.handle_startInstructions(message)
            else:
                self.speak('Okay, i am searching the recipe for {}.'.format(recipeName))
                foundRecipe = self.recipe.loadRecipe(recipeName)
                if foundRecipe:
                    self.speak('I have found a recipe for {}.'.format(recipeName))
                    self.speak('Would you like me to read it?', expect_response=True)
                else:
                    self.speak('I could not find a recipe for {}.'.format(recipeName))
        else:
            self.speak('I could not understand what recipe you want.')
            
    #### INSTRUCTIONS ####

    # called if user confirms to start right after recipe was loaded
    # answer 'yes' to intent before
    @intent_handler(IntentBuilder('yesStartRecipe').require('yesKeyword').require('StartRecipeContext').build())
    @removes_context('StartRecipeContext')
    @adds_context('ListIngredientsContext')
    def handle_yesStartRecipe(self, message):
        self.speak('Would you like to hear the ingredients?', expect_response=True)

    # called if user does not want to start right after recipe was loaded
    # answer 'no' to intent before
    @intent_handler(IntentBuilder('noStartRecipe').require('noKeyword').require('StartRecipeContext').build())
    @removes_context('StartRecipeContext')
    def handle_noStartRecipe(self, message):
        self.speak('Okay, I am here if you want to hear the ingredients and instructions.')


    # called if user wants to hear the recipe
    @intent_handler(IntentBuilder('startInstructions').require('startInstructions'))
    @adds_context('ListIngredientsContext')
    @removes_context('StartRecipeContext')
    def handle_startInstructions(self, message):
        self.speak('Should I list the ingredients first?', expect_response=True)


    # user confirms to her the ingredients first, before reading the instructions
    # answer 'yes' to intent before
    # lists all ingredients, if instructions were read before, asks if user wants to start over again
    # provides next step if instructions were not read before
    @intent_handler(IntentBuilder('YesListIngredients').require('yesKeyword').require('ListIngredientsContext').build())
    @removes_context('ListIngredientsContext')
    @adds_context('StartFromBeginningContext')
    def handle_listIngredients(self, message):
        self.speak(self.recipe.ingredientsToString())
        if self.recipe.loaded and self.recipe.stepCount > 0:
            self.speak('Do you want to start the instructions from the beginning?', expect_response=True)
        else:
            self.speak('Here are the instructions.')
            self.speak(self.recipe.getNextStep())

    # userdoes not want to hear the ingredients first, just wants the steps 
    # answer 'no' to the intent before
    # if instructions were read before, asks user to start over again
    # provides the next step if instructions were not read before
    @intent_handler(IntentBuilder('NoListIngredients').require('noKeyword').require('ListIngredientsContext').build())
    @removes_context('ListIngredientsContext')
    @adds_context('StartFromBeginningContext')
    def handle_doNotListIngredients(self, message):
        self.speak('Okay, i will just tell you the steps.')
        if self.recipe.loaded and self.recipe.stepCount > 0:
            self.speak('Do you want to start from the beginning?', expect_response=True)
        else:
            self.speak(self.recipe.getNextStep())


    # called if user wants to start instructions from the beginning
    # answer 'yes' to intent before
    # provides the first step of method
    @intent_handler(IntentBuilder('YesFromBeginningIntent').require('yesKeyword').require('StartFromBeginningContext').build())
    @removes_context('StartFromBeginningContext')
    def handle_startFromBeginning(self, message):
        self.speak('Okay, i start from the beginning.')
        self.speak(self.recipe.getFirstStep(resetCounter=True))

    # user does not want to start instructions from beginning
    # answer 'no' to intent before
    # provides next step
    @intent_handler(IntentBuilder('NoFromBeginningIntent').require('noKeyword').require('StartFromBeginningContext').build())
    @removes_context('StartFromBeginningContext')
    def handle_doNotStartFromBeginning(self, message):
        self.speak('Okay, here is the next step.')
        self.speak(self.recipe.getNextStep())       

    # returns next step    
    @intent_handler(IntentBuilder('nextStep').require('nextStep'))
    def handle_nextStep(self, message):
        self.speak(self.recipe.getNextStep())
    
    # repeats the previous step
    @intent_handler(IntentBuilder('repeatStep').require('repeatStep'))
    def handle_repeatStep(self, message):
        self.speak(self.recipe.repeatStep())


    #### INGREDIENTS ####

    # lists all ingredients
    @intent_handler(IntentBuilder('getIngredients').require('getIngredients'))
    def handle_getIngredients(self, message):
        self.speak(self.recipe.ingredientsToString())
    
    # returns the amount of asked ingredient
    @intent_handler('get.amount.of.ingredient.intent')
    def handle_getAmountOfIngredient(self, message):
        ingredient = message.data.get('entities', {}).get('ingredient')
        if ingredient is not None:
            self.speak(self.recipe.getAmount(ingredient))
        else:
            self.speak('I could not understand the ingredient.')

        

def create_skill():
    return RecipeSkill()