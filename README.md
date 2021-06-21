# Recipe skill for chatterbox

With this skill, chatterbox can read recipes to you while you are cooking. 
Here is an example:

https://user-images.githubusercontent.com/37368539/122717069-630c0d80-d26b-11eb-926e-b096abedee7b.mp4


## Where do the recipes come from?
Currently, the skill fetches the recipes via http from a local server. Each recipe should have a `json` file in the following structure:
```json
{
  "ingredients": [
    {
      "name":"name of ingredient",
      "amount": 123,
      "unit": "[g/ml/tsp/tbsp/etc.]"
    },
    ...
  ],
  "method": [
    "Step 1",
    "Step 2", 
    ...
  ]  
}
```

Because this skill is not set up with a database, the file name of the recipe has to be the same as you would name it when accessing it. Spaces should be replaced by underscores, for example: _scrambled_tofu.json_ 

## Features 
* **Get Recipe**: chatterbox tries to find a recipe
* **List Ingredients**: chatterbox lists all ingredients with amounts
* **Amount of ingredient**: you can ask for the amount of a single ingredient
* **Start Instructions**: chatterbox starts to read the instructions to you. If you have already started before, chatterbox asks you wheter you want to continue or start from the beginning again.
* **Next step**: chatterbox provides you the next step
* **Repeat step**: chatterbox tells you the previous step again

## Interaction 
The following table contains some example of utterances, the user can say to trigger each functionality. Please have a look at the files located in `locale/en-US/` for a full list of all utterances. 

Intent  | example utterances  |  utterance file
--|---|--
Get recipe  | _"How do I make {recipe_name}"_ <br /> _"Get recipe for {recipe_name}"_ <br /> ...  |  `get.recipe.for.intent`
Start recipe  | _"How do I make it"_ <br /> _"Tell me the instructions"_ <br /> _"Give me the steps"_ <br  /> ...   |  `startInstructions.voc`
List ingredients  | _"What do I need"_ <br /> _"Tell me the ingredients"_ <br /> _"ingredients"_ <br /> ...  | `getIngredients.voc`  
Get amount of ingredient  | _"How much {ingredient} do I need"_ <br /> _"How many {ingredient}"_ <br /> ... | `get.amount.of.ingredient.intent` 
Next step  | _"Tell me the next step"_ <br /> _"next step"_ <br /> _"next"_  |  `nextStep.voc` 
Repeat step  | _"Say that again"_ <br /> _"Repeat step"_ | `repeatStep.voc`  

## Installation and setup
1. Fork this repository.
2. Start a local server to let the chatterbox access your recipes. For example using `python -m SimpleHTTPServer 8989` in the directory of your recipe files.
3. Set the right server address inn the variable `recipeUrl` in the `__init__.py` script. Commit and push the changes to your repository.  
4. Install the skill on your chatterbox posting the command in the chatterbox chat: 
`/install https://github.com/[your_user_name]/chatterbox_recipe_skill` 
