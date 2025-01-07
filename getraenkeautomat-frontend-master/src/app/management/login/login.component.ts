import { Component } from '@angular/core';
import { Router } from '@angular/router';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  error: boolean = false;

  constructor(private router: Router) {
    if (this.hasAuth()) {
      this.router.navigate(['/manager']);
    }
  }

  onSubmit() {
    // Perform authentication here, for example by calling an API
    // If authentication is successful, navigate to the dashboard
    if (this.checkAuth()) {
        this.router.navigate(['/manager']);
      }
    }

  checkAuth() {

    if (this.username === "admin" && this.password === "superSecret") {
      localStorage.setItem("hasAuth", "true");
      this.error = false;

      localStorage.setItem('username', this.username);
      localStorage.setItem('password', this.password);
      
      return true;

  
    }
    localStorage.setItem("hasAuth", "false");
    this.error = true;
    return false;
  }




  hasAuth() {
    if (localStorage.getItem("hasAuth") == "true")
      return true;
    return false;
  
  }

}
