import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { SearchRestService } from '../../services/search-rest.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { VideoBrowsingComponent } from '../video-browsing/video-browsing.component';
import { VideoService } from '../../services/video.service';

@Component({
  selector: 'app-search-engine',
  standalone: true,
  imports: [CommonModule, FormsModule, VideoBrowsingComponent],
  templateUrl: './search-engine.component.html',
  styleUrl: './search-engine.component.css'
})
export class SearchEngineComponent implements OnInit{
  public query = "";

  public constructor(private readonly router: Router, private readonly service : SearchRestService, private readonly videoService : VideoService) {
  }

  // When component is initialized : login to the DRES server & retrieve the current evaluationID
  public ngOnInit() {
    const log = this.service.login("TECHtalent05", "wv6atMjT");
    log.then((response : any) => 
        { this.videoService.sessionId = response.sessionId;
          return this.service.evalId(this.videoService.sessionId);
        })
      .then((response : any) => 
        { this.videoService.evaluationId = response[0].id;
          console.log(this.videoService.evaluationId);
        });
  }

  // Reset the search to its original state
  resetSearch() {
    console.log("reseting");
    this.videoService.keyframeNames.set([]);
    this.query = "";
  }

  // Search for keyframes using the query
  search(){
    console.log("searching for : " + this.query);
    this.service.getVideosFromTextQuery(this.query)
    .then((list : Array<string>) => {
      this.videoService.keyframeNames.set(list);
    })
    .catch((err: unknown) => { console.error("Erreur lors de la récupération des shots : ", err); 
    });
    console.log(this.videoService.keyframeNames)
  }

}
