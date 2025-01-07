import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { LoginComponent } from '../management/login/login.component';
import { Component } from '@angular/core';

@Component({
  selector: '',
  template: ''
})
@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  constructor(private loginComponent: LoginComponent, private router: Router) {}

  canActivate(
    
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {

      const isAuthenticated = this.loginComponent.hasAuth();
    
      if (isAuthenticated) {
        return true;
      } else {
        console.log("fjeifjs");
        this.router.navigate(['/login']);
        return false;
      }
  }
}

export class AuthGuardComponent {

}