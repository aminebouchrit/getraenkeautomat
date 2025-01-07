import { Component, OnInit } from '@angular/core';
import { RecieveService } from '../recieve.service';
import { Bottle } from '../bottle';
import { Subscription } from 'rxjs';
import { IMqttMessage } from 'ngx-mqtt';
import { EventMqttService } from 'src/app/common/event.mqtt.service';
import { BOTTLES } from '../mock-bottles';
import { KeyValue } from '@angular/common';



@Component({
  selector: 'app-bottle',
  templateUrl: './bottle.component.html',
  styleUrls: ['./bottle.component.css']
})
export class BottleComponent implements OnInit {
  selectedBottleIndex: number = 0;

  subscription?: Subscription;
  currency: any;

  emptyBottle: any = {};

  newBottle :any =  {};
  selectedBottle : any = this.emptyBottle;

  bottles: any[] = [];

  constructor(private readonly eventMqtt: EventMqttService) { }



  loadableIndex : number = 0;

  hiddenBottles : Bottle [] = BOTTLES;

  originalOrder = (a: KeyValue<number,string>, b: KeyValue<number,string>): number => {
    return 0;
  }

  trackByFn(index: any, item: any) {
    return index;
 }

 getType(obj: any ){
  return typeof(obj);
 }

  init() {
    this.eventMqtt.setPublishTopic('');
    const mockResponse = {
      response: 'Bottle',
      value: this.hiddenBottles,
    }
    this.eventMqtt.setPublishMessage(mockResponse);
    this.eventMqtt.doPublish();
    }


  sendRequest() {

    this.eventMqtt.setPublishTopic('/get/bottle');
    this.eventMqtt.setPublishMessage({});
    this.eventMqtt.doPublish();
  }

  ngOnInit(): void {
  //  this.init();
  this.sendRequest();

    const myObserver = {
      next: (data : IMqttMessage) => {
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

        this.subscription?.unsubscribe();
        console.log('unsubbed');

      },
      error: (err: Error) => console.error('Observer got an error: ' + err),
      complete: () => {
        console.log('Observer got a complete notification');
        // for (let bottle in this.bottles) {
        //   this.keys[this.loadableIndex] = Object.keys( bottle );
        //   this.values[this.loadableIndex] = Object.values( bottle );
        // }

      },
    };

    this.subscription = this.eventMqtt.subToTopic(myObserver);


//    for (let item of this.bottles[0]) {
 //     this.keys[i] = Object.keys(item);
//      this.values[i] = Object.values(item);

//      i++;
//    }

  }

  getObjectKeys(obj: any): string[] {
    return Object.keys(obj);
  }

  saveChanges() {

    if (this.bottles[this.selectedBottleIndex].bottleID == this.newBottle.bottleID) {

      this.eventMqtt.setPublishTopic('/create/bottle');


      var createMessage = {
        "name": localStorage.getItem('username'),
        "password": localStorage.getItem('password'),
        "value": this.newBottle
            //Hier alle Eigenschaften, die verändert werden sollen, mit neuen Werten

    }

      this.eventMqtt.setPublishMessage(createMessage);
      this.eventMqtt.doPublish();
      return;
    }


    this.eventMqtt.setPublishTopic('/update/bottle');


    var updateMessage = {
        "name": localStorage.getItem('username'),
        "password": localStorage.getItem('password'),
        "bottleID": this.bottles[this.selectedBottleIndex].bottleID,
        "value": this.bottles[this.selectedBottleIndex]
            //Hier alle Eigenschaften, die verändert werden sollen, mit neuen Werten

    }
    this.eventMqtt.setPublishMessage(updateMessage);
    this.eventMqtt.doPublish();

  }

  selectBottle(_t9: number) {
    this.selectedBottleIndex = _t9;
    this.selectedBottle = this.bottles[0];

    // console.log("in select bottle");
    // var i=0;
    // for (let item of this.bottles[0]) {
    //   this.keys[i] = Object.keys(item);
    //   this.values[i] = Object.values(item);
    //   console.log(this.keys[i]); // output parameter names
    //   console.log(this.values[i]); // output parameter values
    //   i++;
    // }

  }

  createNewBottle() {

    let tempNewBottle: typeof BottleComponent.prototype.bottles[0] = {};
    this.newBottle['bottleID'] = this.bottles[this.bottles.length-1].bottleID+1;
    this.newBottle['name'] = 'new Bottle';
//     for (const item of this.bottles[0].slice(1,2).concat(Object.keys(this.bottles[0]).slice(3))) {
//       tempNewBottle[item.keys] = undefined;
//  }

for (const item of Object.keys(this.bottles[0]).slice(1, 2).concat(Object.keys(this.bottles[0]).slice(3))) {
  tempNewBottle[item] = undefined;
}
    this.bottles.push(this.newBottle);


    this.selectBottle(this.bottles.length-1);

    this.newBottle = tempNewBottle;
  }

  deleteBottle(index: number) {

    this.eventMqtt.setPublishTopic('/delete/bottle');


    var deleteMessage = {
        "name": localStorage.getItem('username'),
        "password": localStorage.getItem('password'),
        "bottleID": this.bottles[index].bottleID,
    }

    this.eventMqtt.setPublishMessage(deleteMessage);
    this.eventMqtt.doPublish();


  }

  updateBottle(index: number) {
    const updatedBottle = this.bottles[index];
    // Here, you can write the logic to update data in the backend via MQTT
    // For now, we'll just update the local mock data
 //   this.bottleService.update(this.bottles);
  }

  revertChanges() {
    // Here, you can write the logic to revert changes made to the bottle in the backend via MQTT
    // For now, we'll just reset the bottle to the initial state
    this.bottles = [...this.bottles]; // This will trigger change detection and re-render the component
  }



}
