# Interface Definition for Request/Response with Frontend

For data exchange with the frontend a MQTT broker is being used.<br>

MQTT is not actually intended for classic request/response applications. However, since this technology is already used for communication between the backend and the machine, it is obvious to use the same approach for communication between the backend and the frontend.<br>
As an alternative, the use of websockets was examined. This requires the server to be accessible in the network, which would not have been easy to implement in the THM's eduroam network. Therefore, the approach using MQTT Broker was chosen.<br>

Furthermore, JSON was defined as the data exchange format because it allows data to be structured in objects and is therefore well suited for queries due to its key/value formatting. In addition, there are many libraries and native functions that make working with JSON very easy.<br>

## General Structure of MQTT Topics

Different topics are used to exchange the necessary data with a unique client. The classification of the data is divided into:

- Keyword (e.g. get, create, update, delete, ...)
- Entity (e.g. bottle, order, recipe, machine, ...)

To allow communication with a distinct client, its unique ID is used in the topic as well.

As a generic example, the topic for MQTT messages meant for the backend is structured as follows:
**THM/drinkMachine/client/<clientID\>/<keyword\>/<entity\>**<br>
e. g.: THM/drinkMachine/client/5326785/get/bottle

A message sent to this topic can now contain further information inside a JSON object. Valid keys and values depend on the specific topic and could vary.

A client requests data from the backend via the above topic. It will receive this data or an error message via its own base topic:
**THM/drinkMachine/client/<clientID\>**<br>
With this approach a client only needs to listen to one unique topic and can be sure to subscribe only to data that is valid for him.<br>

## Specific structure of MQTT messages

All allowed requests and their corresponding responses are listed below. If a key is mandatory, it is marked with a star (*). The order of the keywords is not relevant.

request **.../get/category**
```json
{
    //only show categories with a specific parent category
    "parent_categoryID": <integer>
}
```
response:
```json
{
    "response": "category",
    "value": [<Category>,]

}

<Category> {
    "categoryID": <integer>,
    "parent_categoryID": <integer>,
    "name": <string>
}
```

---
request **.../get/bottle**

```json
{
    //only show bottles loaded in specific machines
    "machineID": [<integer>,],
    //only show specific bottles
    "bottleID": [<integer>,],
    //only show bottles within specific categories
    "categoryID": [<integer>,],
    //include bottles with alcohol (default: true)
    "includeAlc": <boolean>
}
```
response:
```json
{
    "response": "bottle",
    "value": [<Bottle>,]
}

<Bottle> {
    "bottleID": <integer>,
    "categoryID": <integer>,
    "name": <string>,
    "density": <float>,
    "max_capacity": <integer>,
    "alcohol_percentage": <float>,
    "price": <float>,
    "pic_url": <string>
}
```

---
request **.../get/recipe**

```json
{
    //only show recipes producable by a specific machine
    "producable_by_machineID": <integer>,
    //only show recipes within specific categories (e.g. Softdrinks)
    "categoryID": [<integer>,],
    //only show recipes that contain specific categories as ingredients (e.g. Cola)
    "contains_categoryID": [<integer>,],
    //include recipes with alcohol (default: true)
    "includeAlc": <boolean>
}
```
response:
```json
{
    "response": "recipe",
    "value": [<Recipe>,]
}

<Recipe> {
    "recipeID": <integer>,
    "categoryID": <integer>,
    "name": <string>,
    "price": <float>,
    "pic_url": <string>,
    "rating_value": <float>,
    "rating_number": <integer>,
    "items": [<RecipeItem>,]
}

<RecipeItem> {
    "categoryID": <integer>,
    "amount_ml": <integer>
}
```

---
request **.../get/machine**
```json
{
    //only show details for specific machines
    "machineID": [<integer>,]
}
```
response:
```json
{
    "response": "machine",
    "value": [<Machine>,]

}

<Machine> {
    "machineID": <integer>,
    "name": <string>,
    "maxGlass": <integer>,
    "contains": [<MachineItem>]
}

<MachineItem> {
    "bottleID": <integer>,
    "position_cm": <integer>,
    "pump_pin": <integer>,
    "led_pin": <integer>,
    "current_capacity": <integer>
}
```

---
request **.../get/glass**

```json
{
    //no filter options
}
```
response:
```json
{
    "response": "glass",
    "value": [<Glass>,]
}

<Glass> {
    "glassID": <integer>,
    "amount_ml": <integer>,
    "weight_g": <integer>
}
```

---
request **.../create/order**

```json
{
    //machine that will produce this order
    *"machineID": <integer>,
    //recipe to be made
    *"recipeID": <integer>
}
```

---
request **.../create/customorder**
```json
{
    //machine that will produce this order
    *"machineID": <integer>,
    //custom ingredients
    *"value": [<OrderItem>,]
}

<OrderItem> {
    *"bottleID": <integer>,
    *"amount_ml": <integer>
}
```

---
request **.../create/rating**
```json
{
    //recipe that will recive this rating
    *"recipeID": <integer>,
    //rating between 1 and 5 stars
    *"rating_value": <integer>
}
```

---
For extended functionality (update, delete, create\*), all clients must specify a username and password.<br>
\*except *.../create/order*, *.../create/customorder* and *.../create/rating*<br>

request **.../create/<ClassName\>**
```json
{
    //username of an admin user
    *"name": <String>,
    //password of an admin user
    *"password": <String>,
    //input values for the new entity
    *"value": [<ClassName>,]
}

<ClassName> {
    //all attributes (without the ID) of the new object to be created
}
```
e.g. request **.../create/bottle**
```json
{
    //username of admin user
    *"name": <String>,
    //password of admin user
    *"password": <String>,
    //input values for a new bottle
    *"value": <NewBottle>
}

<NewBottle> {
    *"categoryID": <integer>,
    *"name": <string>,
    *"density": <float>,
    *"max_capacity": <integer>,
    *"alcohol_percentage": <float>,
    *"price": <float>,
    *"pic_url": <string>
}
```

---
request **.../update/<ClassName\>**
```json
{
    //username of an admin user
    *"name": <String>,
    //password of an admin user
    *"password": <String>,
    //ID of the entity to be changed
    *"<ClassNameID>": <integer>,
    //input values for the updated entity
    *"value": <ClassName>
}

<ClassName> {
    //all attributes to be changed for the existing object
}
```

---
e.g. request **.../update/bottle**
```json
{
    //username of admin user
    *"name": <String>,
    //password of admin user
    *"password": <String>,
    //ID of the bottle to be changed
    *"bottleID": <integer>,
    //input values for new bottle
    *"value": <UpdatedBottle>
}

<UpdatedBottle> {
    "categoryID": <integer>,
    "name": <string>,
    "density": <float>,
    "max_capacity": <integer>,
    "alcohol_percentage": <float>,
    "price": <float>,
    "pic_url": <string>
}
```

---
request **.../delete/<ClassName\>**
```json
{
    //username of an admin user
    *"name": <String>,
    //password of an admin user
    *"password": <String>,
    //ID of the entity to be deleted
    *"<ClassNameID>": <integer>
}
```
e.g. request **.../delete/bottle**
```json
{
    //username of admin user
    *"name": <String>,
    //password of admin user
    *"password": <String>,
    //ID of the bottle to be deleted
    *"bottleID": <integer>
}
```