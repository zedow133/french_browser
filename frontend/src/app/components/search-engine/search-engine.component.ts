import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { SearchRestService } from '../../services/search-rest.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { VideoBrowsingComponent } from '../video-browsing/video-browsing.component';


@Component({
  selector: 'app-search-engine',
  standalone: true,
  imports: [CommonModule, FormsModule, VideoBrowsingComponent],
  templateUrl: './search-engine.component.html',
  styleUrl: './search-engine.component.css'
})
export class SearchEngineComponent {
  public query = "";

  public constructor(private readonly router: Router, private readonly service : SearchRestService) {
  }

  resetSearch() {
    console.log("reseting");
  }

  addQuery(){
    console.log("adding query");
  }

  search(){
    console.log("searching for : " + this.query);
    //  utiliser les queries pour les envoyer dans un service
    // this.service.getVideosFromTextQuery(this.query)
  }

}
