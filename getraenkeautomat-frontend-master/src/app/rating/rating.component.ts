import { Component } from '@angular/core';
import {ItemscountService} from "../service/itemscount.service";
import { EventMqttService } from "../common/event.mqtt.service";


@Component({
  selector: 'app-rating',
  templateUrl: './rating.component.html',
  styleUrls: ['./rating.component.css']
})
export class RatingComponent {

  /**
   * The declaration of necessary variables
   */
  rateDrinks: any[] | null = null;
  recipeId:any;
  ratingNumber:any;


  ngOnInit() {
    this.loadRating();
    localStorage.removeItem('localCart');
    this.itemscount.clear();
  }

  constructor( private itemscount :ItemscountService,  private readonly eventMqtt: EventMqttService) {}


  /**
   * the loadRating function is used to load the shopping cart from local storage
   * and set it as the value of the rateDrinks property.
   */
  loadRating() {
    // get the shopping cart from localStorage
    let shoppingCartString = localStorage.getItem('localCart');
    // if shopping cart is empty, return
    if (!shoppingCartString) {
      return;
    }
    // parse the shopping cart from JSON to JavaScript object
    this.rateDrinks = JSON.parse(shoppingCartString);
  }



  /**
   * Gets the rating for a given recipe and rating number using MQTT.
   * @param recipeId The ID of the recipe to get the rating for.
   * @param ratingNumber The number of the rating to get (1 for first rating, 2 for second rating, etc.).
   * @returns A promise that resolves with the rating value, or rejects with an error message.
   */
  getRating(recipeId: number, ratingNumber: number) {
    this.recipeId=recipeId;
    this.ratingNumber=ratingNumber;
  }

  submitRating(){

    this.eventMqtt.setPublishTopic('/create/rating');
    this.eventMqtt.setPublishMessage({"machineID": Number(localStorage.getItem('machineID')), "recipeID": this.recipeId, "rating_value":this.ratingNumber});
    this.eventMqtt.doPublish();


  }




}
