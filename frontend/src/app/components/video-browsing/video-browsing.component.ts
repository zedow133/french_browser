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
  openVideo(keyframeName : string) {
    this.videoService.currentKeyframeName = keyframeName;

    // Retrieve the video from the keyframe_name
    this.service.getShot(keyframeName)
      .then((shot : any) => {
        this.videoService.currentShot = shot;
        this.videoService.customStartStamp = shot.start_stamp;
        this.videoService.customEndStamp = shot.end_stamp;
      }).then(() => {
        this.router.navigate(['video', this.videoService.trim(keyframeName)])
      });
    
    // Retrieve the similar keyframes to the selected one
    console.log("searching for similar keyshots of video : " + keyframeName);
    this.service.getVideosFromSimilarity(keyframeName)
      .then((list : Array<string>) => {
        this.videoService.similarKeyframes.set(list);
      }).then()
      .catch((err: unknown) => { console.error("Erreur lors de la récupération des shots similaires : ", err); 
      });

    console.log(this.videoService.similarKeyframes)
  }

}