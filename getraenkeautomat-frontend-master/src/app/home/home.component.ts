import {Component, OnInit,Input} from '@angular/core';
import { ItemscountService } from '../service/itemscount.service';
import {Options, LabelType} from "@angular-slider/ngx-slider";
import { EventMqttService } from "../common/event.mqtt.service";
import {Subscription} from "rxjs";
import {IMqttMessage} from "ngx-mqtt";
import {ActivatedRoute , Router} from "@angular/router";


//declare var window:any;
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],

})
export class HomeComponent implements OnInit{


  /**
   * The declaration of necessary variables
   */
  subscriptionDr?: Subscription;
  subscriptionCa?: Subscription;
  subLayerCategoryList: any[] = [];
  allCategoryList: any[] = [];
  drinkList: any[] = [];
  shoppingCart: any[] | null = null;
  drinkInfo: any[] | null = null;
  formModel:any;
  hasRecieveBeenCalled: boolean = false;
  containsAlcohol: number = 0;
  selectedCategoryId: number = 0;

  itemsCart:any = [];
  cartNumber:number = 0;

  firstAllCatCall: boolean = false;

  /**
   * The price slider object with its minimum and maximum values, and configuration options.
   */
  priceSlider = {
    /**
     * The minimum value of the price slider.
     */
    minValue: 0,

    /**
     * The maximum value of the price slider.
     */
    maxValue: 5,
    /**
     * The configuration options for the price slider.
     */

    options: {
      /**
       * The minimum value of the slider scale.
       */
      floor: 0,

      /**
       * The step increment for the slider.
       */
      step:0.2,

      /**
       * The maximum value of the slider scale.
       */
      ceil: 5,

      /**
       * The function that returns the label to be displayed for each slider value.
       * @param value The slider value.
       * @param label The label type (low, high, or none).
       * @returns The label to be displayed for the specified value and label type.
       */
      translate: (value: number, label: LabelType): string => {
        switch (label) {
          case LabelType.Low:
            return '<b>Min: </b>'+ value+ '€';
          case LabelType.High:
            return '<b>Max: </b>'+ value+ '€';
          default:
            return value + ' €';
        }
      }
    }
  };


  /**
   * Lifecycle hook that is called after Angular has initialized all data-bound properties of the directive.
   * Sets the machine ID from the URL, checks for any saved machines, requests layer 1 categories,
   * and loads the shopping cart from local storage.
   */
  ngOnInit() {
    // Sets the machine ID from the URL
    this.setMachineIdFromUrl();

    // Checks for any saved machines
    this.checkSavedMachine();

    // Requests layer 1 categories
    this.requestLayer1Categories();

    // Loads the shopping cart from local storage
    this.loadShoppingCart();



    
    const drink ={
      response: 'drink',
      value: '',
    }
    //5 alles in Init setzen und aufrufen
    /*this.eventMqtt.setPublishMessage(category);
    this.eventMqtt.doPublish();
    this.generateCategories();*/
  }


  /**
   * Constructs a new instance of the component.
   * @param itemscount The service responsible for managing the item count in the shopping cart.
   * @param eventMqtt The service responsible for handling MQTT events.
   * @param route The currently activated route.
   * @param router The router service.
   */
   constructor(
     private itemscount :ItemscountService,
     private readonly eventMqtt: EventMqttService,
     private route: ActivatedRoute,
     private router: Router) {}


  /**
   * Sets the machine ID from the URL parameter to the local storage if it is present.
   * Uses the currently activated route to get the parameter.
   */
  setMachineIdFromUrl() {
    const machineid = this.route.snapshot.paramMap.get('id');
    if (machineid)
      localStorage.setItem("machineID", machineid+'');
  }


  /**
   * Checks if a machine ID has been saved in local storage. If not, navigates to the machine selection page.
   * Skips check if the 'debug' key is set to '1' in local storage.
   */
  checkSavedMachine(){
    const debugKey = localStorage.getItem('debug');

    if(debugKey && debugKey == '1')
      return;

    const machineid = localStorage.getItem('machineID');

    if(machineid == null){
      this.router.navigate(['/machineSelection']);
    }
  }

  removeUnusedTopCategories() {
    let hitCategories:boolean[] = new Array(this.subLayerCategoryList.length);
    for (let i=0; i < this.subLayerCategoryList.length; i++) {
      for (let drink of this.drinkList) {
        if ( this.subLayerCategoryList[i].categoryID == this.getTopLevelCategory(drink.categoryID)) {

          hitCategories[i] = true;
        }
      }
    }
    console.log(hitCategories);
    for (let i=hitCategories.length;i>-1; i--) {
      if (hitCategories[i] != true) {
        this.subLayerCategoryList.splice(i, 1);
        console.log("deleted Category: %d", i);
      }

      
    }
  }

  getTopLevelCategory(categoryID: number): number {
    for (let category of this.allCategoryList) {
      if( category.categoryID == categoryID ) {
       if (category.parent_categoryID == 1)
        return category.categoryID;


      return this.getTopLevelCategory(category.parent_categoryID);
      }
    }
    return 0;

  }


  /**
   * This method is used to send a request to the server to get all the categories available.
   * The request is sent using MQTT protocol.
   */
  sendAllCategoriesRequest() {
    this.eventMqtt.setPublishTopic('/get/category');
    this.eventMqtt.setPublishMessage({});
    this.eventMqtt.doPublish();
  }

  /**
   * This function is used to send a request to the MQTT broker to get all the layer-1 categories of products.
   * The function sets the topic to /get/category and sets the parent_categoryID property in the message object
   * to 1, which means it requests the categories whose parent category is the root category.
   * Then the function publishes the message by calling the doPublish() method of the EventMqttService
   */
  sendLayer1CategoriesRequest() {
    this.subLayerCategoryList = [];
    this.drinkList = [];
    this.allCategoryList = [];
    this.firstAllCatCall = false;
    this.hasRecieveBeenCalled = false;

    this.eventMqtt.setPublishTopic('/get/category');
    this.eventMqtt.setPublishMessage({'parent_categoryID': 1});
    this.eventMqtt.doPublish();
  }

  /**
   * This method sends an MQTT request to get the list of producible drinks for a given category ID and machine ID.
   * It sets the MQTT publish topic to /get/recipe, and sets the publish message to an object with properties categoryID
   * and producable_by_machineID based on the input arguments categorieID and localStorage.getItem("machineID"), respectively.
   *
   * @param categorieID A number representing the ID of the category for which the producible drinks are requested.
   */
  sendProduceableDrinksRequest(categorieID : number) {
    this.eventMqtt.setPublishTopic('/get/recipe');
    if (this.containsAlcohol == 2)
      this.eventMqtt.setPublishMessage({"categoryID": [categorieID], "producable_by_machineID": Number(localStorage.getItem("machineID")), "includeAlc": false});
    else
      this.eventMqtt.setPublishMessage({"categoryID": [categorieID], "producable_by_machineID": Number(localStorage.getItem("machineID"))});
    this.eventMqtt.doPublish();
  }

  /**
   * This function sends a request to the MQTT broker to retrieve the drinks that belong to the specified category ID for debugging purposes.
   * The MQTT topic '/get/recipe' is set as the publishing topic and the message sent with the request is a JSON object containing the category ID.
   * The MQTT message is sent using the 'doPublish()' method of the 'eventMqtt' instance.
   *
   * @param categorieID a number representing the ID of the category for which the request for drinks is being made.
   */
  sendDebugDrinksRequest(categorieID : number) {
    this.eventMqtt.setPublishTopic('/get/recipe');
    if (this.containsAlcohol == 2)
    this.eventMqtt.setPublishMessage({"categoryID": [categorieID], "includeAlc": false});
    else
      this.eventMqtt.setPublishMessage({"categoryID": [categorieID]});
    this.eventMqtt.doPublish();
  }

  /**
   * This method sends a request to retrieve the layer 1 category of the drinks recipes available for the selected machine.
   * It calls the sendLayer1CategoriesRequest() method to send the request using the MQTT service,
   * and then calls the recieveCategories() method to receive and process the response.
   */
  requestLayer1Categories() {
    this.sendLayer1CategoriesRequest();
    this.recieveCategories();
  }

  /**
   * This function is a method of an Angular component/service and is used to request all categories from the server using MQTT protocol.
   * It first sets the publishing topic to "/get/category", sets the publishing message to an empty object, and then publishes the message using
   * an instance of the EventMqttService.
   */
  requestAllCategories() {
    this.sendAllCategoriesRequest();
    this.recieveAllCategories();
  }


  /**
   * Requests a list of produceable drinks for a given category ID, and receives the response.
   * If the debug flag is set, sends a request for all drinks instead.
   *
   * @param categorieID The ID of the category for which to retrieve drinks.
   */
  requestProduceableDrinks(categorieID : number){

    // If this function has already been called, do not execute again
    if (this.hasRecieveBeenCalled){
      return;
    }
    // Clear the existing drink list
    this.drinkList = [];

    // If the debug flag is set, send a request for all drinks instead
    const debugKey = localStorage.getItem('debug');
    if(debugKey && debugKey == '1') {
      this.sendDebugDrinksRequest(categorieID);
    }

    else
      this.sendProduceableDrinksRequest(categorieID);

    // Receive the response and populate the drink list
    this.recieveDrinks();
    // Set the flag to indicate that this function has been called
    this.hasRecieveBeenCalled = true;
  }

  /**
   * Subscribes to the topic for receiving all categories from the MQTT broker.
   */
  recieveAllCategories() {
    // Subscribes to the topic and sets up a callback for when a message is received
    this.subscriptionCa = this.eventMqtt.subToTopic(
      // Callback function for handling received messages
      (data : IMqttMessage) => {
        // Parses the received message as JSON

        let response = JSON.parse(data.payload.toString());
        // Checks if there was an error in the response
        if(response.response == 'Error'){
          console.error('error:', response.value);
          return;
        }
        console.log('Observer got a next value: ' + response);

        // Checks if the response is for the correct topic
        if(response.response !== 'category') {
          return;
        }

        // Adds each category to the list of all categories
        for (let item of response.value) {
          this.allCategoryList.push(item);
         // console.log(item);
        }

        // Unsubscribes from the topic after receiving the categories
        this.subscriptionCa?.unsubscribe();
        console.log('unsubbed');
        console.log(this.allCategoryList);
        if(!this.firstAllCatCall) {
          this.firstAllCatCall = true;
          this.removeUnusedTopCategories();
        }
      }
    );
  }


  /**
   * Subscribes to MQTT topic for receiving layer 1 categories and saves them in subLayerCategoryList.
   * After receiving the categories, sends requests for getting the producible drinks and all categories.
   * Unsubscribes from the MQTT topic after receiving the categories.
   */
  recieveCategories() {
    this.subscriptionCa = this.eventMqtt.subToTopic(
      (data : IMqttMessage) => {
        let response = JSON.parse(data.payload.toString());
        if(response.response == 'Error'){
          console.error('error:', response.value);
          return;
        }

        console.log('Observer got a next value: ' + response);

        if(response.response !== 'category') {
          return;
        }

//


           for (let item of response.value) {
             this.subLayerCategoryList.push(item);
           }



        this.requestProduceableDrinks(1);
        this.subscriptionCa?.unsubscribe();
        console.log('unsubbed');
        this.requestProduceableDrinks(1);
        this.requestAllCategories();


      }
    );

  }

  /**
   * This function subscribes to the topic '/get/recipe' and listens to incoming messages.
   * When a message is received, it parses the payload and checks if the response is an error.
   * If it is not an error, it checks if the response is a recipe.
   * If it is a recipe, it adds each item in the response value to the drinkList array.
   * The function then unsubscribes from the topic and logs a message.
   */
   recieveDrinks(){
    this.subscriptionDr = this.eventMqtt.subToTopic(
      (data : IMqttMessage) => {
        let response = JSON.parse(data.payload.toString());
        if(response.response == 'Error'){
          console.error('error:', response.value);
          return;
        }

        console.log('Observer got a next value: ' + response);

        if(response.response !== 'recipe') {
          return;
        }
        for (let item of response.value) {
          this.drinkList.push(item);
          console.log(item);

        }
         this.subscriptionDr?.unsubscribe();
        console.log('unsubbed');
      


      }
    );
      console.log(this.drinkList)
    console.log(this.allCategoryList)

    for(let drink of this.drinkList){
      // Variable to temporarily store the parent_categoryID
      let temp_parent_categoryID;

      // Search all categories in allCategoryList for the given category ID
      for(var j of this.allCategoryList){
        if(j.categoryID == drink.categoryID){
          temp_parent_categoryID = j.parent_categoryID;
        }
      }
      // Search all categories in allCategoryList for the parent_categoryID and return the name
      for(var j of this.allCategoryList){
        if(j.categoryID == temp_parent_categoryID){
          return j.name;
        }
      }}


  }


  /**
   * Returns the name of the category that belongs to the specified category ID.
   *
   * @param categorieID The ID of the category whose name should be returned.
   * @returns The name of the category, if found, otherwise null.
   */

  getCategoryName(categorieID: number){
    // Variable to temporarily store the parent_categoryID
    let temp_parent_categoryID;

    // Search all categories in allCategoryList for the given category ID
    for(var j of this.allCategoryList){
      if(j.categoryID == categorieID){
        temp_parent_categoryID = j.parent_categoryID;
      }
    }
    // Search all categories in allCategoryList for the parent_categoryID and return the name
    for(var j of this.allCategoryList){
      if(j.categoryID == temp_parent_categoryID){
        return j.name;
      }
    }
  }

  /**
   * Loads the shopping cart from local storage.
   */
  loadShoppingCart() {
    // Retrieve the shopping cart from local storage
    let shoppingCartString = localStorage.getItem('localCart');

    // If the shopping cart is not found in local storage, return
    if (!shoppingCartString) {
      return;
    }

    // Parse the shopping cart string as JSON and set it as the shopping cart
    this.shoppingCart = JSON.parse(shoppingCartString);
  }

  /**
   * Adds a drink item to the shopping cart or increases its quantity if it already exists.
   *
   * @param recievedDrink The drink item to be added to the cart.
   */
  addItemToCart(recievedDrink: any) {
    // Check if the shopping cart is empty or undefined
    if (!this.shoppingCart || this.shoppingCart.length == 0) {
      // If so, create a new shopping cart and add the drink item with a quantity of 0
      this.shoppingCart = [];
      this.shoppingCart.push({'drink': recievedDrink, 'quantity': 1});
    }
    else {
      // If the shopping cart already contains items, search for the drink item
      for (let shoppingCartEntry of this.shoppingCart) {
        if (shoppingCartEntry.drink.recipeID == recievedDrink.recipeID) {
          // If the drink item is found, increase its quantity and exit the loop
          shoppingCartEntry.quantity++;
          break;
        }
        else {
          // If the drink item is not found, add it with a quantity of 1 and exit the loop
          this.shoppingCart.push({'drink': recievedDrink, 'quantity': 1});
          break;
        }
      }
    }

    // Save the shopping cart to local storage and update the items count
    localStorage.setItem('localCart', JSON.stringify(this.shoppingCart));
    this.itemscount.increment();
  }



  /**
   * Handles the change event of the 'Yes' checkbox for alcohol content.
   * Important: function not implemented from backend. Ignoring setting
   * 
   * @param event The change event object.
   */
  onAlcoholYesCheckboxChange(event: any) {
    // Check if the 'Yes' checkbox is checked
    if (event.target.checked) {
      // If so, set the alcohol content flag to true
      this.containsAlcohol =1;

    } else {
      // If not, set the alcohol content flag to false
      this.containsAlcohol =0;
    }
  }

  /**
   * Handles the change event of the 'No' checkbox for alcohol content.
   *
   * @param event The change event object.
   */
  onAlcoholNoCheckboxChange(event: any) {
    // Check if the 'No' checkbox is checked
    if (event.target.checked) {
      // If so, set the alcohol content flag to 2
      this.containsAlcohol =2;
      this.requestLayer1Categories();

    } else {
      // If not, set the alcohol content flag to 0
      this.containsAlcohol =0;
      this.requestLayer1Categories();
    }
  }


  openDrinkInformation(recievedDrink: any)
  {
    // Check if the shopping cart is empty or undefined
    if (!this.drinkInfo || this.drinkInfo.length == 0)
    {
      this.drinkInfo = [];
      this.drinkInfo.push({'drink': recievedDrink});
    }

    // Save the shopping cart to local storage and update the items count
    localStorage.setItem('drinkInfo', JSON.stringify(this.drinkInfo));
    this.itemscount.increment();
  }




}
