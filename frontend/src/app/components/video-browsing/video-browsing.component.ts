import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { SearchRestService } from '../../services/search-rest.service';

@Component({
  selector: 'app-video-browsing',
  standalone: true,
  imports: [],
  templateUrl: './video-browsing.component.html',
  styleUrl: './video-browsing.component.css'
})
export class VideoBrowsingComponent {

  public constructor(private readonly router: Router, private readonly service : SearchRestService) {
    }
    
  openVideo() {
    this.router.navigate(['video', 'salut'])
  }

}
