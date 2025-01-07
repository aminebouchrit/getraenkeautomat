import { Component } from '@angular/core';

@Component({
  selector: 'app-information',
  templateUrl: './information.component.html',
  styleUrls: ['./information.component.css']
})
export class InformationComponent {

  /**
   * The declaration of necessary variables
   */
  drinkInfo: any[] | null = null;

  ngOnInit():void
  {
    this.loadDrinkInfo();
  }

  /**
   * Load drink information from local storage.
   * This function retrieves drink information from local storage and
   * populates the `drinkInfo` property of the component with the data.
   * If no drink information is found in local storage, this function
   * does nothing.
   */
  loadDrinkInfo() {
    let shoppingCartString = localStorage.getItem('drinkInfo');
    if (!shoppingCartString) {
      return;
    }
    this.drinkInfo = JSON.parse(shoppingCartString);
  }
}
