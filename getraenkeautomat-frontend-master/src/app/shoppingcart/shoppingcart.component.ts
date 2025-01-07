import { Component , OnInit } from '@angular/core';
import { ItemscountService } from '../service/itemscount.service';
import { EventMqttService } from "../common/event.mqtt.service";
import {Subscription} from "rxjs";
import {IMqttMessage} from "ngx-mqtt";


@Component({
  selector: 'app-shoppingcart',
  templateUrl: './shoppingcart.component.html',
  styleUrls: ['./shoppingcart.component.css']
})
export class ShoppingcartComponent implements OnInit{

  /**
   * The declaration of necessary variables
   */
  shoppingCart: any[] | null = null;



constructor(private itemscount :ItemscountService,  private readonly eventMqtt: EventMqttService) {
}


  ngOnInit():void
  {
    this.loadShoppingCart();
  }


  /**
   * This function loads the user's shopping cart from local storage. It retrieves
   * the shopping cart data from the 'localCart' key in the local storage and parses
   * the data into a JavaScript object. If the 'localCart' key is not present in
   * the local storage, this function simply returns without performing any action.
   * Once the shopping cart data is parsed into an object,
   * it is stored in the this.shoppingCart property of the class instance.
   */
  loadShoppingCart() {
    let shoppingCartString = localStorage.getItem('localCart');
    if (!shoppingCartString) {
      return;
    }
    this.shoppingCart = JSON.parse(shoppingCartString);
  }


  /**
   * Calculates the total volume of a mixture from a list of ingredients.
   * @param ingredientList: An array of ingredients, where each ingredient has an 'amount_ml' property indicating the amount in milliliters.
   * @returns totalVolume: The total volume of the mixture in milliliters.
   */
  getMixVolume(ingredientList: any[]){
    let totalVolume = 0;
    for (let ingredient of ingredientList) {
      totalVolume += ingredient.amount_ml;
    }
    return totalVolume;
  }


  /**
   * Calculates the total price of a mixture from a list of ingredients.
   * @param   ingredientList: An array of ingredients, where each ingredient has a 'price' property indicating the price of the ingredient.
   * @returns totalPrice: The total price of the mixture.
   */
  getMixPrice(ingredientList: any[]){
    let totalPrice = 0;
    for (let ingredient of ingredientList) {
      totalPrice += ingredient.price;
    }
    return totalPrice;
  }


  /**
   * Calculates the total price of all items in the shopping cart.
   * @returns totalPrice The total price of all items in the shopping cart.
   */
  getTotalPrice() {
    if (!this.shoppingCart)
      return 0;

    let totalPrice = 0;
    for (let shoppingCartEntry of this.shoppingCart) {

      if (shoppingCartEntry.drink.recipeID) {
        totalPrice += shoppingCartEntry.drink.price.toFixed(2) * (shoppingCartEntry.quantity);
        continue;
      }
      totalPrice += this.getMixPrice(shoppingCartEntry.drink.ingredients) * (shoppingCartEntry.quantity);
    }
    return totalPrice;
  }


  /**
   * Increases the quantity of an item in the shopping cart by 1.
   * @param  shoppingCartEntry: The item in the shopping cart to increase the quantity of.
   */
  increaseItemQuantity(shoppingCartEntry: any) {
    shoppingCartEntry.quantity++;
    this.itemscount.increment();
    localStorage.setItem('localCart',JSON.stringify(this.shoppingCart));
  }


  /**
   * Decreases the quantity of an item in the shopping cart by 1.
   * @param  shoppingCartEntry: The item in the shopping cart to decrease the quantity of.
   */
  decreaseItemQuantity(shoppingCartEntry: any) {
    if (shoppingCartEntry.quantity > 1) {
      shoppingCartEntry.quantity--;
      this.itemscount.decrement();
      localStorage.setItem('localCart',JSON.stringify(this.shoppingCart));
    }
  }

  /**
   * Deletes a single item from the shopping cart.
   * @param index: The index of the item to delete.
   */
  singleDelete (index: number) {
    if (!this.shoppingCart) {
      this.itemscount.clear();
      return;
    }
    this.itemscount.decrement(this.shoppingCart[index].quantity);
    this.shoppingCart?.splice(index, 1);
    localStorage.setItem('localCart', JSON.stringify(this.shoppingCart));
  }


  /**
   * This function is used to place an order for items in the shopping cart.
   * It first checks if there is a shopping cart available, and if not, it returns.
   * Then, it loops through each item in the shopping cart and checks if it is a custom
   * drink or a pre-made drink.
   */
  toOrder(){
    if (!this.shoppingCart)
      return;

    for (let shoppingCartEntry of this.shoppingCart) {
      console.log(shoppingCartEntry);
      if (shoppingCartEntry.drink.mixName) {
        const ingridients = [];
        //Order for mixed drinks
        this.eventMqtt.setPublishTopic('/create/customorder');
        for (let i=0;i<=shoppingCartEntry.quantity; i++) {
          this.eventMqtt.setPublishMessage({"machineID": Number(localStorage.getItem('machineID')), "value": shoppingCartEntry.drink.ingredients});
          this.eventMqtt.doPublish();
        }
        return;
      }
      //Order for simple drinks
      this.eventMqtt.setPublishTopic('/create/order')
      for (let i=0;i<=shoppingCartEntry.quantity; i++) {
        this.eventMqtt.setPublishMessage({"machineID": Number(localStorage.getItem('machineID')), "recipeID": shoppingCartEntry.drink.recipeID});
        this.eventMqtt.doPublish();
      }
    }

  }


}
