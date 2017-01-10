<h1>Alexa skill - PowerCo v1.0</h1>
This skill allows PowerCo Energy customers to check their recent bill and energy usage.
Launch the skill by saying "Launch PowerCo" or "Open PowerCo." The interaction is described below.
<p>

<ol>
<li>The program will first ask you to authenticate with
a 4-digit PIN. In this version, the PIN has been hardcoded as "9876"</li> 
<li>Once authenticated, the skill will then list the addresses that are
associated with your account</li>
<li>Choose one of the addresses by saying the number that corresponds to the address, like "Account number two."</li>
<li>Alexa will then read the account detail, including the current amount due and due date</li>
</ol>
 
<h2>Source Files</h2>
Source files included in this repository are as follows:

<b>PowerCo.py</b><br>
This is the Python source code for the Lambda function that powers the skill.
<br>

<b>IntentSchema.json</b><br>
This schema defines the intents and word formats for which our skill will listen. This code needs to be entered into the skill configuration on the Alexa page of your Amazon Developer Account.
<br>

<b>PowerCoAPITest.py</b><br>
This is Python code that is used to test how a JSON object is returned from an API and processed for use by the Alexa skill.
<br>

<b>SampleUtterances.txt</b><br>
This code needs to be entered into the skill configuration on the Alexa page of your Amazon Developer Account.

<b>deployToLambda.sh</b>
bash script to package and deploy PowerCo.py to Lambda using your local AWS account credentials. You'll need your access_key_id and secret_access_key. See this link to setup your local AWS account credentials if needed: http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-config-files

<h2>Deployment</h2>
Unfortunately, AWS CloudFormation isnt able to deploy to the Alexa Skills Kit at this time. To deploy PowerCo, follow these steps:<br>
<ol>
<li>Create the Lambda function called PowerCo.</li>
<li>Create an Alexa Skill in the Amazon Developer Portal with the configuration in ASK-Config.txt</li>
<li>Visit alexa.amazon.com to activate the account on your Echo device.</li>
<li>Say "Alexa, open PowerCo" !
</ol>

<h2>Future Improvements</h2>
<b>Account Linking</b><br>
Add account linking when signing up for the skill.
