import { CommonModule } from '@angular/common';
import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { VideoService } from '../../services/video.service';
import { SearchRestService } from '../../services/search-rest.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-overview-video',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './overview-video.component.html',
  styleUrl: './overview-video.component.css'
})

export class OverviewVideoComponent {
  videoSrc = 'assets/sample-video.mp4'; // Replace with your actual video path
  keyframes: string[] = [];
  query = "";

  constructor(public readonly router : Router, public readonly videoService : VideoService, public readonly service : SearchRestService){

  }

  homepage(){
    this.router.navigate([''])
  }
  
  submitText() {
    console.log('Submitted text:', this.query);
  }

  onSubmitVideoAction() {
    this.service.submitVideo(this.videoService.evaluationId, this.videoService.sessionId, this.videoService.trim(this.videoService.currentShot), 1, 2);
    // 1 -> start
    // 2 -> end
  }

  openVideo(shotId : string){
    this.videoService.currentShot = shotId;
    
    console.log("searching for similar keyshots of video : " + shotId);
    this.service.getVideosFromSimilarity(shotId)
      .then((list : Array<string>) => {
        this.videoService.similarShots.set(list);
      })
      .catch((err: unknown) => { console.error("Erreur lors de la récupération des shots similaires : ", err); 
      });

    console.log(this.videoService.similarShots)
    this.router.navigate(['video', shotId])
  }
  
}


