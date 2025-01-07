import { Component, OnInit } from '@angular/core';
import { RecieveService } from '../recieve.service';
import { Bottle } from '../bottle';
import { Subscription } from 'rxjs';
import { IMqttMessage } from 'ngx-mqtt';
import { EventMqttService } from 'src/app/common/event.mqtt.service';
import { BOTTLES } from '../mock-bottles';
import { KeyValue } from '@angular/common';

@Component({
  selector: 'app-category',
  templateUrl: './category.component.html',
  styleUrls: ['./category.component.css']
})
export class CategoryComponent implements OnInit {
createNewRecipe() {
throw new Error('Method not implemented.');
}
  selectedCategoryIndex: number = 0;

  subscription?: Subscription;
  currency: any;

    
  selectedCategory : any = {};
  newCategory : any = {};

  categories: any[] = [];

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
      response: 'Bottle',
      value: this.hiddenBottles,
    }
    this.eventMqtt.setPublishMessage(mockResponse);
    this.eventMqtt.doPublish();
    }

  sendRequest(parent : number | null) {

    this.eventMqtt.setPublishTopic('/get/category');
    this.eventMqtt.setPublishMessage({"parent_categoryID": parent});
    this.eventMqtt.doPublish();
  }

  ngOnInit(): void {
  //  this.init();
  console.log('dvdvs');
    this.sendRequest(1);
    console.log('dvdvs');
    const myObserver = {
      next: (data : IMqttMessage) => {
        let response = JSON.parse(data.payload.toString());
        if(response.response == 'Error') {
          console.error('error :', response.value);
          return;
        }
        if(response.response !== 'category') {
          return;
        }
        console.log('Observer got a next value: ' + response.value);

        for (let item of response.value) {
          this.categories.push(item);
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

    if (this.categories[this.selectedCategoryIndex].bottleID == this.newCategory.bottleID) {
    
      this.eventMqtt.setPublishTopic('/create/category');
      

      var createMessage = {
        "username": localStorage.getItem('username'),
        "password": localStorage.getItem('password'),
        "value": this.newCategory
            //Hier alle Eigenschaften, die verändert werden sollen, mit neuen Werten
        
    }

      this.eventMqtt.setPublishMessage(createMessage);
      this.eventMqtt.doPublish();
      return;
    }
    

    this.eventMqtt.setPublishTopic('/update/category');
      

    var updateMessage = {
        "username": localStorage.getItem('username'),
        "password": localStorage.getItem('password'),
        "bottleID": this.selectedCategoryIndex,
        "value": this.categories[this.selectedCategoryIndex]
            //Hier alle Eigenschaften, die verändert werden sollen, mit neuen Werten
        
    }

    this.eventMqtt.setPublishMessage(updateMessage);
    this.eventMqtt.doPublish();
  



  }

  selectCategory(_t9: number) {
    this.selectedCategoryIndex = _t9;
    this.selectedCategory = this.categories[this.selectedCategoryIndex];

    this.categories = [];
    this.categories.push(this.selectedCategory);
    this.sendRequest(this.selectedCategory.categoryID);

    this.ngOnInit();
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

  createNewCategory() {

    this.newCategory['bottleID'] = this.categories[this.categories.length-1].bottleID+1;
    this.newCategory['name'] = 'new Bottle';
    for (const item of Object.keys(this.categories[0]).slice(1,2).concat(Object.keys(this.categories[0]).slice(3))) {
      this.newCategory[item] = undefined;
 }

    this.categories.push(this.newCategory);


    
  }

  deleteCategory(index: number) {
    
    this.eventMqtt.setPublishTopic('/delete/category');
      

    var deleteMessage = {
        "username": localStorage.getItem('username'),
        "password": localStorage.getItem('password'),
        "bottleID": this.categories[index].bottleID,
    }

    this.eventMqtt.setPublishMessage(deleteMessage);
    this.eventMqtt.doPublish();
  

  }

  updateBottle(index: number) {
    const updatedBottle = this.categories[index];
    // Here, you can write the logic to update data in the backend via MQTT
    // For now, we'll just update the local mock data
 //   this.bottleService.update(this.bottles);
  }

  revertChanges() {
    // Here, you can write the logic to revert changes made to the bottle in the backend via MQTT
    // For now, we'll just reset the bottle to the initial state
    this.categories = [...this.categories]; // This will trigger change detection and re-render the component
  }


  
}
