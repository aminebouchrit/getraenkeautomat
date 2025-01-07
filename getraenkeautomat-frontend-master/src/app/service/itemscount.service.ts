import { Injectable } from '@angular/core';
import { of, Subject } from 'rxjs' ;

@Injectable({
  providedIn: 'root'
})
export class ItemscountService {

  constructor() { }

  cartCounter = 0;
  cartSubject = new Subject<any>();



  increment() {
    this.cartCounter++;
    this.cartSubject.next(this.cartCounter);
  }

  decrement(amount?: number) {
      if (this.cartCounter > 0) {
        this.cartCounter -= amount ? amount : 1;

        this.cartSubject.next(this.cartCounter);
        return;
      }

  }

  clear() {
    this.cartCounter = 0;
    this.cartSubject.next(0);
  }

  setCartCounter(shoppingCart: any[]) {
    for (let shoppingCartEntry of shoppingCart) {
       this.cartCounter += shoppingCartEntry.quantity;  
    }
    this.cartSubject.next(this.cartCounter);
  }
}
