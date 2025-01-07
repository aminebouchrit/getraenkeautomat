import { Component , OnInit} from '@angular/core';
import { Router } from '@angular/router';
import { ReqSendService } from '../common/req.send.service';
import { ItemscountService } from '../service/itemscount.service';

@Component({
  selector: 'app-order',
  templateUrl: './order.component.html',
  styleUrls: ['./order.component.css']
})
export class OrderComponent implements OnInit{

  /**
   * The declaration of necessary variables
   */
  oderNr: number;
  currentDate: string;
  getOrderDetails:any=[];
  orderTyp : number | undefined;

  shoppingCart: any[] | null = null;


  constructor(private itemscount :ItemscountService, private reqSendService: ReqSendService,  private router: Router) {
    // generate a random number between 1 and 100
    this.oderNr = Math.floor(Math.random() * 100000000) + 1;
    // get the current date and format it as a string
    this.currentDate = new Date().toLocaleDateString();

  }

  ngOnInit(): void {
    this.loadShoppingCart();
    console.log(this.shoppingCart);

    this.reqSendService.requestAllCategories();
    this.reqSendService.requestAllDrinks();

    // localStorage.removeItem('localCart');
    // this.itemscount.clear();
  }

  /**
   * Loads the shopping cart from local storage and sets it to the `shoppingCart` property.
   * If the shopping cart is not present in local storage, the function does nothing.
   */
  loadShoppingCart() {
    // get the shopping cart from localStorage
    let shoppingCartString = localStorage.getItem('localCart');
    // if shopping cart is empty, return
    if (!shoppingCartString) {
      return;
    }
    // parse the shopping cart from JSON to JavaScript object
    this.shoppingCart = JSON.parse(shoppingCartString);
  }


  getCategoryName(categoryID: number): string {
    console.log(this.reqSendService.getAllCategories());
    for (let category of this.reqSendService.getAllCategories()) {
      if (category.categoryID == categoryID)
        return category.name;

    }
    return "";
  }

  getDrinkName(recipeID: number): string {
    for (let drink of this.reqSendService.getAllDrinks()) {
      if (drink.recipeID == recipeID)
        return drink.name;

    }
    return "";
  }

  getTotalPrice(shoppingCartEntry:any){
    let totalPrice = 0;


    for (let ingredient of shoppingCartEntry.drink.ingredients) {
      totalPrice += ingredient.price;
    }
    return totalPrice;
  }

  getTotalVolume(shoppingCartEntry:any){
    let totalVolume = 0;

    if (shoppingCartEntry.drink.recipeID) {
      for (let item of shoppingCartEntry.drink.items) {
        totalVolume += item.amount_ml;
      }
      return totalVolume;
    }

    for (let ingredient of shoppingCartEntry.drink.ingredients) {
      totalVolume += ingredient.amount_ml;
    }
    return totalVolume;
  }

  loadOrder(){
    if (localStorage.getItem('localCart')){
      this.oderNr=0;
      // @ts-ignore
      this.getOrderDetails = JSON.parse(localStorage.getItem('localCart'));
    }
  }

  goToHome() {
    localStorage.removeItem('localCart');
    this.itemscount.clear();

    this.router.navigate(['/']);

  }

}
