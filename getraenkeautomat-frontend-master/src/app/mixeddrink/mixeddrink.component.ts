import { Component, ViewChild, ElementRef, OnInit } from '@angular/core';
import { Subscription } from "rxjs";
import { IMqttMessage } from "ngx-mqtt";

import { ItemscountService } from "../service/itemscount.service";
import { EventMqttService } from "../common/event.mqtt.service";

@Component({
  selector: 'app-mixeddrink',
  templateUrl: './mixeddrink.component.html',
  styleUrls: ['./mixeddrink.component.css']
})


export class MixeddrinkComponent implements OnInit{

  subscriptionBottle?: Subscription;

  constructor( private itemscount :ItemscountService, private readonly eventMqtt: EventMqttService) {}

  volumeSlider = {
    value: 30,
    options: {
      floor: 5,
      ceil: 100,
      step: 5,
      showTicks: true,
      tickStep: 25
    }
  };


  /**
   * The declaration of necessary variables
   */
  bottles: any = [] ;
  shoppingCart: any[] | null = null;
  ingredients: any[] = [];
  mixName: string = '';
  selectedBottleID: number = -1;

  ngOnInit(){
    this.requestBottles();
    this.loadShoppingCart();

  }

  sendBottleRequest() {
    this.eventMqtt.setPublishTopic('/get/bottle');
    this.eventMqtt.setPublishMessage({"machineID": [Number(localStorage.getItem("machineID"))]});
    this.eventMqtt.doPublish();
  }

  sendDebugBottleRequest() {
    this.eventMqtt.setPublishTopic('/get/bottle');
    this.eventMqtt.setPublishMessage({});
    this.eventMqtt.doPublish();
  }

  /**
   * Sends a request for bottle information to the server and subscribes to the response topic to receive the bottle information.
   * If debug mode is enabled, sends a debug request instead of a regular request.
   * Calls recieveBottles() to subscribe to the response topic and receive the bottle information.
   */
  requestBottles() {
    const debugKey = localStorage.getItem('debug');
    if(debugKey && debugKey == '1')
      this.sendDebugBottleRequest();
    else
      this.sendBottleRequest();

    this.recieveBottles();
  }

  /**
   * Subscribes to the MQTT topic for receiving bottles and processes the received data.
   * Unsubscribes from the topic after processing the data.
   */
  recieveBottles(): void {
    this.subscriptionBottle = this.eventMqtt.subToTopic(
      (data : IMqttMessage) => {
        let response = JSON.parse(data.payload.toString());
        if(response.response == 'Error') {
          console.error('error :', response.value);
          return;
        }
        if(response.response !== 'bottle') {
          return;
        }
        console.log('Observer got a next value: ' + response);

        for (let item of response.value) {
          this.bottles.push(item);
          console.log(item);

        }

        this.subscriptionBottle?.unsubscribe();
        console.log('unsubbed');

      }
    );

  }

  /**
   * This function loads the shopping cart from the local storage if it exists.
   */
  loadShoppingCart() {
    // Get the shopping cart string from the local storage
    let shoppingCartString = localStorage.getItem('localCart');

    // If the shopping cart string does not exist, return
    if (!shoppingCartString) {
      return;
    }

    // Parse the shopping cart string and store it in the shopping cart variable
    this.shoppingCart = JSON.parse(shoppingCartString);
  }

  /**
   * Selects a bottle with the given bottleID for the drink with the given drinkName and price.
   *
   * @param drinkName: A string representing the name of the drink.
   * @param price:  A number representing the price of the drink.
   * @param bottleID:  A number representing the ID of the bottle to be selected.
   */
  selectBottle(drinkName:string, price:number, bottleID: number)
  {
    this.selectedBottleID=bottleID;
  }

  /**
   * This function retrieves the price of a bottle based on its ID.
   * @param bottleID: A number representing the ID of the bottle for which to retrieve the price.
   * @return bottle.price: A number representing the price of the bottle with the specified ID.
   * If no bottle with the specified ID is found, 0 is returned.
   */
  getBottlePrice(bottleID: number): number {
    for (let bottle of this.bottles) {
      if (bottle.bottleID == bottleID)
        return bottle.price;
    }
    return 0;
  }


  /**
   * This function searches for a bottle in the bottles array that matches the given bottleID parameter.
   * If a matching bottle is found, its name is returned. If no matching bottle is found, an empty string is returned.
   * @param bottleID: a number representing the ID of the bottle to retrieve the name for.
   * @return bottle.name: a string representing the name of the bottle corresponding to the given bottleID.
   * If no bottle is found with the given ID, an empty string is returned.
   */
  getBottleName(bottleID: number): string {
    for (let bottle of this.bottles) {
      if (bottle.bottleID == bottleID)
        return bottle.name;
    }
    return '';
  }

  /**
   * This function adds a new ingredient to the list of ingredients for a drink.
   * It retrieves the currently selected bottle ID, volume, price, and name using
   * helper functions and pushes a new ingredient object into the ingredients array.
   */
   addIngredient() {
    if (this.selectedBottleID == -1)
      return;
    this.ingredients.push({
      bottleID: this.selectedBottleID,
      amount_ml: this.volumeSlider.value,
      price: (this.getBottlePrice(this.selectedBottleID)*this.volumeSlider.value)/100,
      name: this.getBottleName(this.selectedBottleID)
    });
  }

  /**
   * This function returns a default name for a new mix. If the shopping cart is empty,
   * the default name is "new Mix 1". If the shopping cart is not empty, the default name is "new Mix"
   * followed by a number that is one greater than the number of existing mixes in the cart.
   * @return string containing the default name for a new mix
   */
  getDefaultMixName() {
    if (!this.shoppingCart) {
      return 'new Mix 1';
    }
    let mixCount = 0;
    for (let shoppingCartEntry of this.shoppingCart) {
      if (shoppingCartEntry.drink.mixName)
        mixCount++;
    }
    return 'new Mix '+(mixCount+1);
  }


  /**
   * This function calculates and returns the total price of all the ingredients added to the shopping cart.
   * It first initializes the totalPrice variable to zero and then iterates through the list of ingredients,
   * adding the price of each ingredient to the totalPrice. Finally, it returns the totalPrice.
   */
  getTotalPrice(){
    let totalPrice = 0;
    for (let ingredient of this.ingredients) {
      totalPrice += ingredient.price;
    }
    return totalPrice;
  }


  /**
   * This function calculates and returns the total volume of all ingredients in the shopping cart.
   * @return totalVolume: The total volume of all ingredients in milliliters.
   */
  getTotalVolume(){
    let totalVolume = 0;
    for (let ingredient of this.ingredients) {
      totalVolume += ingredient.amount_ml;
    }
    return totalVolume;
  }

  /**
   * This function deletes a given ingredient from the list of ingredients in the shopping cart.
   * It takes an ingredient as an argument which is of type any. It finds the index of the ingredient
   * in the array using the indexOf() method and then removes it from the array using the splice() method.
   * @param ingredient
   */
  deleteIngredient(ingredient:any) {
    const index = this.ingredients.indexOf(ingredient);
    if (index !== -1) {
      this.ingredients.splice(index, 1);
    }
  }


  /**
   * This function clears the current mix by resetting the list of ingredients to an empty array,
   * setting the selectedBottleID to -1, and resetting the mixName to an empty string.
   */
  clearMix() {
    this.ingredients=[];
    this.selectedBottleID = -1;
    this.mixName = '';
  }


  /**
   * This function is used to add the current custom drink to the shopping cart.
   * If the custom drink has not been named, it will be assigned
   * a default name based on the number of existing mixes in the cart.
   * The custom drink is then added to the cart or the quantity of an existing mix is incremented.
   * The shopping cart is saved in the local storage and the mix is cleared.
   * The number of items in the shopping cart is incremented.
   */
  addToCart(){
    if (this.ingredients.length == 0)
      return;

    if (this.mixName == '')
      this.mixName = this.getDefaultMixName();

    let customDrink = {
      drink: {
        mixName: this.mixName,
        ingredients: this.ingredients
      },
      quantity: 1
    };

    if(!this.shoppingCart) {
      this.shoppingCart = [];
      this.shoppingCart.push(customDrink);
      localStorage.setItem('localCart', JSON.stringify(this.shoppingCart));
      return;
    }
    for(let shoppingCartEntry of this.shoppingCart) {
      if (shoppingCartEntry.drink.mixName == customDrink.drink.mixName) {
        shoppingCartEntry.quantity++;
        break;
      }

    }
    this.shoppingCart.push(customDrink);
    localStorage.setItem('localCart', JSON.stringify(this.shoppingCart));


    this.itemscount.increment();
    this.clearMix();
  }

}
