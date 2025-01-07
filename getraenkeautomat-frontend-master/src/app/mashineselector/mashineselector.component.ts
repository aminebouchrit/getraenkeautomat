import { Component,OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { EventMqttService } from "../common/event.mqtt.service";
import {Subscription} from "rxjs";
import {IMqttMessage} from "ngx-mqtt";

@Component({
  selector: 'app-mashineselector',
  templateUrl: './mashineselector.component.html',
  styleUrls: ['./mashineselector.component.css']
})
export class MashineselectorComponent implements OnInit{

  /**
   * The declaration of necessary variables
   */
  subscriptionMa?: Subscription;
  machines: any [] = [];


  constructor(private router: Router, private readonly eventMqtt: EventMqttService){}


  ngOnInit(){

    this.requestMachines();

  }

  sendMachinesRequest() {
    this.eventMqtt.setPublishTopic('/get/machine');
    this.eventMqtt.setPublishMessage({});
    this.eventMqtt.doPublish();
  }

  requestMachines() {
    this.sendMachinesRequest();
    this.recieveMachines();
  }


  /**
   * The recieveMachines() function subscribes to a topic using MQTT (Message Queuing Telemetry Transport) protocol
   * and waits for messages. When a message is received, it checks if the response type is "machine".
   * If it is, it extracts the machine information from the message and adds it to an array called machines.
   * The subscription is then unsubscribed. If there is an error response, it logs the error message to the console.
   */
  recieveMachines() {
    this.subscriptionMa = this.eventMqtt.subToTopic(
      (data : IMqttMessage) => {
        let response = JSON.parse(data.payload.toString());
        if(response.response == 'Error'){
          console.error('error:', response.value);
          return;
        }

        console.log('Observer got a next value: ' + response);

        if(response.response !== 'machine') {
          return;
        }
        for (let item of response.value) {
          // leeres Array wird verwendet
          this.machines.push(item);
          console.log(item);

        }
        this.subscriptionMa?.unsubscribe();
        console.log('unsubbed');

      }
    );

  }


  /**
   * This method selectMachine() takes a machine ID as a parameter and navigates to the corresponding
   * machine's page by setting the route to /machineID/machineID where machineID is the actual ID of the machine.
   * @param machineID
   */
  selectMachine(machineID: Number){
    localStorage.removeItem('debug');
    this.router.navigate(['/machineID/'+machineID])
  }


  /**
   * This method startDebugMode() method sets a local storage variable "debug" to "1", removes "machineID"
   * from local storage and navigates the user to the root path using the Angular router.
   */
  startDebugMode() {
    localStorage.setItem('debug', '1');
    localStorage.removeItem('machineID');
    this.router.navigate(['']);
  }

}
