import { CommonModule } from '@angular/common';
import { Component, Input, Output, EventEmitter, OnInit, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
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

export class OverviewVideoComponent implements AfterViewInit {
  @ViewChild('mainVideo', { static: false }) mainVideo!: ElementRef<HTMLVideoElement>;

  constructor(public readonly router : Router, public readonly videoService : VideoService, public readonly service : SearchRestService){
  }
  
  submitText() {
    console.log('Submitted text:', this.query);
  }

  onSubmitVideoAction() {
    this.service.submitVideo(this.videoService.evaluationId, this.videoService.sessionId, this.videoService.trim(this.videoService.currentShot), 1, 2);
    // 1 -> start
    // 2 -> end
  }

  // Fonction pour définir le start stamp personnalisé
  setCustomStart() {
    if (this.mainVideo && this.mainVideo.nativeElement) {
      this.videoService.customStartStamp = this.mainVideo.nativeElement.currentTime * 1000; // Convertir en millisecondes
      console.log('Custom start stamp set to:', this.videoService.customStartStamp);
    }
  }

  // Fonction pour définir le end stamp personnalisé
  setCustomEnd() {
    if (this.mainVideo && this.mainVideo.nativeElement) {
      this.videoService.customEndStamp = this.mainVideo.nativeElement.currentTime * 1000; // Convertir en millisecondes
      console.log('Custom end stamp set to:', this.videoService.customEndStamp);
    }
  }

  openVideo(shotId : string){
    this.videoService.currentShotID = shotId;
    
    this.service.getShot(shotId)
    .then((shot : any) => {
      this.videoService.currentShot = shot;
    }).then(() => {
      this.router.navigate(['video', shotId])
    })

    console.log("searching for similar keyshots of video : " + shotId);
    this.service.getVideosFromSimilarity(shotId)
      .then((list : Array<string>) => {
        this.videoService.similarShots.set(list);
      })
      .catch((err: unknown) => { console.error("Erreur lors de la récupération des shots similaires : ", err); 
      });

    console.log(this.videoService.similarShots)
  }
  
}


