import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { SearchRestService } from '../../services/search-rest.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { VideoBrowsingComponent } from '../video-browsing/video-browsing.component';
import { VideoService } from '../../services/video.service';
import { response } from 'express';


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

  resetSearch() {
    console.log("reseting");
    this.videoService.shots.set([]);
    this.query = "";
  }

  addQuery(){
    console.log("adding query");
  }

  search(){
    console.log("searching for : " + this.query);
    //  utiliser les queries pour les envoyer dans un service
    this.service.getVideosFromTextQuery(this.query)
    .then((list : Array<string>) => {
      this.videoService.shots.set(list);
    })
    .catch((err: unknown) => { console.error("Erreur lors de la récupération des shots : ", err); 
    });
    console.log(this.videoService.shots)
  }

}
