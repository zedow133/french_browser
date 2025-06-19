import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { SearchRestService } from '../../services/search-rest.service';
import { CommonModule } from '@angular/common';
import { VideoService } from '../../services/video.service';

@Component({
  selector: 'app-video-browsing',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './video-browsing.component.html',
  styleUrl: './video-browsing.component.css'
})
export class VideoBrowsingComponent {

  public constructor(private readonly router: Router, public readonly service : SearchRestService, public readonly videoService : VideoService) {
  }
    
  // Open the video selected 
  openVideo(shotId : string) {
    this.videoService.currentShotID = shotId;

    // Retrieve the video from the shotID
    this.service.getShot(shotId)
      .then((shot : any) => {
        this.videoService.currentShot = shot;
        this.videoService.customStartStamp = shot.start_stamp;
        this.videoService.customEndStamp = shot.end_stamp;
      }).then(() => {
        this.router.navigate(['video', shotId])
      });
    
    // Retrieve the similar keyframes to the selected one
    console.log("searching for similar keyshots of video : " + shotId);
    this.service.getVideosFromSimilarity(shotId)
      .then((list : Array<string>) => {
        this.videoService.similarShots.set(list);
      }).then()
      .catch((err: unknown) => { console.error("Erreur lors de la récupération des shots similaires : ", err); 
      });

    console.log(this.videoService.similarShots)
  }

}