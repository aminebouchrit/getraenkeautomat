import { Component , OnInit } from '@angular/core';
import { ItemscountService } from '../service/itemscount.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent  implements OnInit{
  cartCounter:number = 0;

  constructor( private itemscount :ItemscountService, private router: Router)
  {
    this.itemscount.cartSubject.subscribe((data)=>{
      this.cartCounter=data;
    });
  }


  inDebugMode() {
    const debugKey = localStorage.getItem('debug');
    if(debugKey && debugKey == '1')
      return true;
    return false;
  }

  ngOnInit(): void {
    this.initCartCounter();
  }

  initCartCounter(){
    let shoppingCartString = localStorage.getItem('localCart');
    if(!shoppingCartString)
      return;
    let shoppingCart = JSON.parse(shoppingCartString);
    this.itemscount.setCartCounter(shoppingCart);
    
  }



  goToManager() {

    this.router.navigate(['/login']);


  }

  goToHome() {

    this.router.navigate(['/']);


  }

  goToCart() {

    this.router.navigate(['/shopping_cart']);

  }

  goToMachine(){
    this.router.navigate(['/machineSelection']);
  }
}
