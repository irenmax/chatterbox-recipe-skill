# Recipe skill for chatterbox

With this skill, chatterbox can read recipes to you while you are cooking. 
Here is an example:

https://user-images.githubusercontent.com/37368539/122717069-630c0d80-d26b-11eb-926e-b096abedee7b.mp4


## Where do the recipes come from?
Currently, the skill fetches the recipes via http from a local server. The recipes have to be in `json` format with the following properties:


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
