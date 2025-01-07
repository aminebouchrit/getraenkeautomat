import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { AuthGuard } from './common/authguard.component';
import { AppRoutingModule } from './app-routing.module';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon'
import { AppComponent } from './app.component';
import { ManagementComponent } from './management/management.component';
import { HomeComponent } from './home/home.component';
import { NavbarComponent } from './navbar/navbar.component';
import { ShoppingcartComponent } from './shoppingcart/shoppingcart.component';
import { FooterComponent } from './footer/footer.component';
import { RatingComponent } from './rating/rating.component';
import { LoginComponent } from './management/login/login.component';
import { CurrencyPipe } from '@angular/common';
import { BottleComponent } from './management/bottle/bottle.component';
import { IMqttServiceOptions, MqttModule } from "ngx-mqtt";
import { mqttEnv as env } from './common/enviroment';
import { EventMqttService } from './common/event.mqtt.service';
import { ReqSendService } from './common/req.send.service';
import { MashineComponent } from './management/mashine/mashine.component';
import { CategoryComponent } from './management/category/category.component';
import { MixeddrinkComponent } from './mixeddrink/mixeddrink.component';
 import {NgxSliderModule} from "@angular-slider/ngx-slider";
import { OrderComponent } from './order/order.component';
import { InformationComponent } from './information/information.component';
import { MashineselectorComponent } from './mashineselector/mashineselector.component';

const MQTT_SERVICE_OPTIONS: IMqttServiceOptions = {
  hostname: env.server,
  port: env.port,
  protocol: (env.protocol === "wss") ? "wss" : "ws",
  path: env.path,
  clean: env.clean,
  clientId: env.clientId,
  connectTimeout: env.connectTimeout,
  reconnectPeriod: env.reconnectPeriod
};

@NgModule({
  declarations: [
    AuthGuard,
    AppComponent,
    ManagementComponent,
    HomeComponent,
    NavbarComponent,
    ShoppingcartComponent,
    FooterComponent,
    LoginComponent,
    RatingComponent,
    BottleComponent,
    MashineComponent,
    CategoryComponent,
    BottleComponent,
      MixeddrinkComponent,
      OrderComponent,
      InformationComponent,
    MashineselectorComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    FormsModule,
    RouterModule,
    CurrencyPipe,
    MatIconModule,
    MqttModule.forRoot(MQTT_SERVICE_OPTIONS),
    NgxSliderModule
  ],
  providers: [LoginComponent, EventMqttService, ReqSendService],
  bootstrap: [AppComponent]
})
export class AppModule {  }
