import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-search-engine',
  standalone: true,
  imports: [],
  templateUrl: './search-engine.component.html',
  styleUrl: './search-engine.component.css'
})
export class SearchEngineComponent {

  public constructor(private readonly router: Router) {
  }
  openVideo() {
    this.router.navigate(['video', 'salut'])
  }

}
