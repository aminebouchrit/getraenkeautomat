import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent }   from './home/home.component';
import { ManagementComponent } from './management/management.component';
import { ShoppingcartComponent } from './shoppingcart/shoppingcart.component';
import { RatingComponent } from './rating/rating.component';
import { AuthGuard } from './common/authguard.component';
import { LoginComponent } from "./management/login/login.component";
import { MashineComponent } from './management/mashine/mashine.component';
import { BottleComponent } from './management/bottle/bottle.component';
import { CategoryComponent } from './management/category/category.component';
import { MixeddrinkComponent} from "./mixeddrink/mixeddrink.component";
import {OrderComponent} from "./order/order.component";
import {InformationComponent} from "./information/information.component";
import {MashineselectorComponent} from "./mashineselector/mashineselector.component";


const routes: Routes = [
  { path: ""  ,             component :HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'manager', component: ManagementComponent, canActivate: [AuthGuard] },
  { path: "shopping_cart" , component :ShoppingcartComponent },
  { path: "order" ,        component :OrderComponent},
  { path: 'mashines', component: MashineComponent, canActivate: [AuthGuard] },
  { path: "bottles" , component : BottleComponent, canActivate: [AuthGuard]  },
   { path: "categories" ,        component : CategoryComponent, canActivate: [AuthGuard]  },
  { path: "mixeddrink"  ,             component :MixeddrinkComponent },
   { path: "categories" ,        component : CategoryComponent, canActivate: [AuthGuard]},
  { path: "mixeddrink"  ,             component :MixeddrinkComponent },
  {path: "rating", component: RatingComponent},
  {path: "information", component: InformationComponent},
  {path: "machineSelection", component: MashineselectorComponent},
  { path: 'machineID/:id'  ,             component :HomeComponent }
 ];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
