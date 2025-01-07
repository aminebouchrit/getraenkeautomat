import { Component, OnInit } from '@angular/core';
import { mqttEnv } from './common/enviroment';


@Component({
  selector: 'home-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'getraenkeautomat-frontend';


  ngOnInit() : void{
    localStorage.setItem('clientId', mqttEnv.clientId);
    console.log(localStorage.getItem('clientId'));
  }
}
