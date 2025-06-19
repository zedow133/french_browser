import { Component } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'French Browser !';

  constructor(public readonly router : Router){
  }
  
  // Routing to the homepage when clicking on the app name
  homepage(){
    this.router.navigate([''])
  }
}
