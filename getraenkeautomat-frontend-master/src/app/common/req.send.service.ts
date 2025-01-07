import { Injectable } from '@angular/core';
import { EventMqttService } from "../common/event.mqtt.service";
import { Subscription } from "rxjs";
import { IMqttMessage } from "ngx-mqtt";

@Injectable({
  providedIn: 'root'
})
export class ReqSendService {
  subscriptionCa?: Subscription;
  subscriptionDr?: Subscription;
  
  drinkList: any[] = [];
  allCategoryList: any[] = [];

  constructor(private readonly eventMqtt: EventMqttService) { }

  sendAllCategoriesRequest() {
    this.eventMqtt.setPublishTopic('/get/category');
    this.eventMqtt.setPublishMessage({});
    this.eventMqtt.doPublish();
  }

  sendAllDrinksRequest() {
    this.eventMqtt.setPublishTopic('/get/recipe');
    this.eventMqtt.setPublishMessage({});
    this.eventMqtt.doPublish();
  }

  requestAllDrinks() {
    this.sendAllDrinksRequest();
    this.recieveDrinks();
  }

  requestAllCategories() {
    this.sendAllCategoriesRequest();
    this.recieveAllCategories();
  }

  recieveAllCategories() {
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
        for (let item of response.value) {
          this.allCategoryList.push(item);
          console.log(item);

        }
        //4 empfangen der Daten
        this.subscriptionCa?.unsubscribe();
        console.log('unsubbed');

      }
    );

  }

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
          // 3 cateG array o. Mock nutzen
          this.drinkList.push(item);
          console.log(item);

        }
        //4 empfangen der Daten
        this.subscriptionDr?.unsubscribe();
        console.log('unsubbed');

      }
    );

  }

  getAllCategories() {
    return this.allCategoryList;
  }

  getAllDrinks() {
    return this.drinkList;
  }
}
