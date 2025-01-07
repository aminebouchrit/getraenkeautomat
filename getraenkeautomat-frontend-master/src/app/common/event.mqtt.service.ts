import { Injectable } from '@angular/core';
import { IMqttMessage, MqttService, IPublishOptions } from "ngx-mqtt";
import { Observable, Observer, Subscribable } from "rxjs";
import { Subscription } from 'rxjs';
import { IClientSubscribeOptions } from 'mqtt-browser';

interface Subable {
  topic: string,
  conOptions: {
    qos: number
  }
  messages: string[];
}

@Injectable()
export class EventMqttService {


  /**
   * The declaration of necessary variables
   */
  baseTopic : string = 'THM/drinkMachine';

  publish = {
    topic: this.baseTopic,
    conOptions: {
      qos: 0,
      retain: false
    },
    payload: '{}',
  };

  subscribe: Subable =  {
    topic: this.baseTopic,
    conOptions: {
      qos: 0
    },
    messages: []
  };
  hasConnetion = false;

  /**
   * // Set the initial subscribe and publish topics to empty strings
   * @param _mqttService is a private property of the class that is an instance of the MqttService class.
   */
  constructor(private _mqttService: MqttService) {
    // Get the client ID from local storage
    var clientId = localStorage.getItem('clientId');
    // If the client ID is null, log an error message
    if (clientId == null)
      console.error('Could not get clientId');
    // Set the base topic for this MQTT client
    this.baseTopic = this.baseTopic+'/client/'+clientId;
    // Set the initial subscribe and publish topics to empty strings
    this.setSubscribeTopic('');
    this.setPublishTopic('');
 }


  /**
   * The doPublish() function you provided seems to be using the unsafePublish()
   * function of the _mqttService object to publish an MQTT message.
   */
  doPublish() {
    console.log(this.publish)
    this._mqttService.unsafePublish(this.publish.topic, this.publish.payload, this.publish.conOptions as IPublishOptions );
   }

  subToTopic(observerOrNext?: Partial<Observer<IMqttMessage>> | ((value: IMqttMessage) => void)): Subscription  {

    return this._mqttService.observe(this.subscribe.topic, this.subscribe.conOptions as IClientSubscribeOptions).subscribe(observerOrNext);

 }


  /**
   * The destroyConnection() function appears to be used to disconnect from the MQTT broker
   * and clean up any resources used by the MQTT client.
   */
  destroyConnection() {
    try {
      // Disconnect from the MQTT broker
      this._mqttService.disconnect(true);
      // Set the connection status to false
      this.hasConnetion = false;
      console.log('Successfully disconnected!')
    } catch (error: any) {
      console.log('Disconnect failed', error.toString())
   }}


  /**
   * Sets the MQTT topic that will be used when publishing a message.
   * @param topic A string representing the topic that the message should be published to.
   */
  setPublishTopic(topic: String) {
    // Combine the base topic and the specified topic to form the full topic to publish to
    this.publish.topic = this.baseTopic+''+topic;
  }

  /**
   * Sets the MQTT topic that will be used when subscribing a message.
   * @param topic A string representing the topic that the message should be dubscribed to.
   */
  setSubscribeTopic(topic: String) {
    this.subscribe.topic = this.baseTopic+''+topic;
  }


  /**
   * Sets the message payload for an MQTT publish message.
   *
   * @param object - The object to use as the payload for the message.
   */
  setPublishMessage( object: any ) {
    // Set the message payload to the JSON stringified version of the object
    this.publish.payload = JSON.stringify( object );
  }
}
