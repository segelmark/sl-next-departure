# sl-next-departure
The Alexa skill that checks the next departure of SL local transportation from a certain stop.

### How to use
* "Ask SL when does the next metro leave"
* "Ask SL when does bus 4 leave"

### How to set up
1. Set up your skill in the [Amazon Developer Console](https://developer.amazon.com/alexa):
   * Go to the Amazon Developer Console and sign in with your Amazon Developer account
   * Click on "Create Skill" in the upper-right corner
   * Choose a skill model, "Custom" for a unique skill, give your skill a name and choose a default language
2. Configure your skill's interaction model:
   * In the "Interaction Model" section, you'll define the intents, sample utterances, and slot types for your skill
   * Use the JSON Editor to upload the interaction model or Skill Builder create your skill's interaction model
3. Develop your skill's backend logic:
   * Choose a hosting method for your skill's backend code, such as AWS Lambda
4. Test and use your skill:
   * Use the built-in test simulator in the Alexa Developer Console to test your skill's functionality
   * You use your skill on an Alexa-enabled device by enabling it for testing in the "Distribution" section of the console

### Voice interface

#### Invocation Name
The invocation name for the skill is 'S. L.' used to begin interacting with the skill.

#### Intents
The intent represents an action that fulfills a user's spoken request. Intents can optionally have arguments called slots.
* DepartureInfoIntent

#### Sample Utterances
A sample utterance is a spoken phrase that a user might say to invoke an intent 

* "When does {linenumber} leave"
* "When does {transportationmode} {linenumber} leave"
* "When does the next {transportationmode} leave"

#### Slots
Slot is a placeholder for a piece of information that the user will provide when making a request

* A custom intent to provide departure information based on transportation mode and line number. It has the following slots:
* linenumber: This is a slot of type 'AMAZON.NUMBER'. It is used to capture the line number of the transportation mode.
* transportationmode: This is a slot of type 'transportmodes'. It is used to capture the mode of transportation like bus, train, metro, etc.
