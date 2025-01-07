import { Component, OnInit } from '@angular/core';
import { RecieveService } from '../recieve.service';
import { Bottle } from '../bottle';
import { Subscription } from 'rxjs';
import { IMqttMessage } from 'ngx-mqtt';
import { EventMqttService } from 'src/app/common/event.mqtt.service';
import { BOTTLES } from '../mock-bottles';
import { KeyValue } from '@angular/common';

@Component({
  selector: 'app-mashine',
  templateUrl: './mashine.component.html',
  styleUrls: ['./mashine.component.css']
})
export class MashineComponent implements OnInit {
  selectedMachineIndex: number = 0;

  subscription?: Subscription;
  currency: any;

  
  selectedMachine : any = {};
  newMachine : any = {};

  machines: any[] = [];

  constructor(private readonly eventMqtt: EventMqttService) { }

  

  loadableIndex : number = 0;

  hiddenBottles : Bottle [] = BOTTLES;
 
  originalOrder = (a: KeyValue<number,string>, b: KeyValue<number,string>): number => {
    return 0;
  }

  trackByFn(index: any, item: any) {
    return index;
 }

  init() {
    const mockResponse = {
      response: 'Machine',
      value: this.hiddenBottles,
    }
    this.eventMqtt.setPublishMessage(mockResponse);
    this.eventMqtt.doPublish();
    }


    sendRequest() {

      this.eventMqtt.setPublishTopic('/get/machine');
      this.eventMqtt.setPublishMessage({});
      this.eventMqtt.doPublish();
    }

  ngOnInit(): void {
   // this.init();

    this.sendRequest();

    const myObserver = {
      next: (data : IMqttMessage) => {
        let response = JSON.parse(data.payload.toString());
        if(response.response == 'Error') {
          console.error('error :', response.value);
          return;
        }
        console.log('Observer got a next value: ' + response);
        if(response.response !== 'machine') {
          return;
        }
     

        for (let item of response.value) {
          this.machines.push(item);
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


  isArray(obj : any ) {
    return Array.isArray(obj)
 }

  saveChanges() {

    if (this.machines[this.selectedMachineIndex].bottleID == this.newMachine.bottleID) {
    
      this.eventMqtt.setPublishTopic('/create/machine');
      

      var createMessage = {
        "username": localStorage.getItem('username'),
        "password": localStorage.getItem('password'),
        "value": this.newMachine
            //Hier alle Eigenschaften, die verändert werden sollen, mit neuen Werten
        
    }

      this.eventMqtt.setPublishMessage(createMessage);
      this.eventMqtt.doPublish();
      return;
    }
    

    this.eventMqtt.setPublishTopic('/update/machine');
      

    var updateMessage = {
        "username": localStorage.getItem('username'),
        "password": localStorage.getItem('password'),
        "bottleID": this.selectedMachineIndex,
        "value": this.machines[this.selectedMachineIndex]
            //Hier alle Eigenschaften, die verändert werden sollen, mit neuen Werten
        
    }

    this.eventMqtt.setPublishMessage(updateMessage);
    this.eventMqtt.doPublish();
  



  }

  selectMachine(_t9: number) {
    this.selectedMachineIndex = _t9;
    this.selectedMachine = this.machines[0];

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

  createNewMachine() {

    this.newMachine['bottleID'] = this.machines[this.machines.length-1].bottleID+1;
    this.newMachine['name'] = 'new Bottle';
    for (const item of Object.keys(this.machines[0]).slice(1,2).concat(Object.keys(this.machines[0]).slice(3))) {
      this.newMachine[item] = undefined;
 }

    this.machines.push(this.newMachine);


    
  }

  deleteMachine(index: number) {
    
    this.eventMqtt.setPublishTopic('/delete/machine');
      

    var deleteMessage = {
        "username": localStorage.getItem('username'),
        "password": localStorage.getItem('password'),
        "bottleID": this.machines[index].bottleID,
    }

    this.eventMqtt.setPublishMessage(deleteMessage);
    this.eventMqtt.doPublish();
  

  }

  updateMachines(index: number) {
    const updatedBottle = this.machines[index];
    // Here, you can write the logic to update data in the backend via MQTT
    // For now, we'll just update the local mock data
 //   this.bottleService.update(this.bottles);
  }

  revertChanges() {
    // Here, you can write the logic to revert changes made to the bottle in the backend via MQTT
    // For now, we'll just reset the bottle to the initial state
    this.machines = [...this.machines]; // This will trigger change detection and re-render the component
  }


  
}
