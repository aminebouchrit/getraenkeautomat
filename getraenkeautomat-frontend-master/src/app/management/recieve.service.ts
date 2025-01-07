import { Injectable } from '@angular/core';
import { Observable, Observer, of } from 'rxjs';
import { delay } from 'rxjs/operators';
import { Bottle } from './bottle';
import { BOTTLES } from './mock-bottles';
import { Subscription } from 'rxjs';
import { IMqttMessage } from "ngx-mqtt";
import { EventMqttService } from '../common/event.mqtt.service';

@Injectable({
  providedIn: 'root'
})
export class RecieveService {
  events: any[] = [];

  hiddenBottles : Bottle [] = BOTTLES;
 
  

  constructor(private readonly eventMqtt: EventMqttService) { 

  }

  init() {
    this.eventMqtt.setPublishMessage(this.hiddenBottles);
    this.eventMqtt.doPublish();
    }

  destroy(): void {
      if (this.eventMqtt) {
          this.eventMqtt.destroyConnection();
      }
  }
  update(bottleList: object[]) {
  
    
    console.log("Your MoM");
    // this.mqttManager.createConnection();
    // this.mqttManager.doPublish();
    //this.hiddenBottles = bottleList;
    
  
  }

  subscribeToTopic(observerOrNext?: Partial<Observer<IMqttMessage>> | ((value: IMqttMessage) => void) ) : Subscription {
    // return this.eventMqtt.subToTopic(
    //   (data: IMqttMessage) => {
    //       let item = JSON.parse('['+data.payload.toString()+']');
    //   console.log(this.events);
    //   this.events.push(item);
    // });
    return this.eventMqtt.subToTopic(observerOrNext);

  }

}
