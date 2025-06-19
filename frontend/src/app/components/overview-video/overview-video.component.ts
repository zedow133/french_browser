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

  ngAfterViewInit() {
    // Écouter l'événement loadedmetadata pour s'assurer que la vidéo est chargée
    if (this.mainVideo && this.mainVideo.nativeElement) {
      this.mainVideo.nativeElement.addEventListener('loadedmetadata', () => {
        this.setVideoToStartStamp();
      });
      
      // Si la vidéo est déjà chargée
      if (this.mainVideo.nativeElement.readyState >= 1) {
        this.setVideoToStartStamp();
      }
    }
  }

  setVideoToStartStamp() {
    if (this.videoService.currentShot && this.videoService.currentShot.start_stamp && this.mainVideo) {
      const startTimeInSeconds = this.videoService.currentShot.start_stamp / 1000;
      this.mainVideo.nativeElement.currentTime = startTimeInSeconds;
    }
  }

  onSubmitVideoAction() {
    const confirmed = window.confirm('Are you sure you want to submit?');
    if (confirmed) {
      console.log('Submitting...');
      this.service.submitVideo(this.videoService.evaluationId, this.videoService.sessionId, this.videoService.trim(this.videoService.currentShotID), this.videoService.customStartStamp, this.videoService.customEndStamp);
    }
  }

  // Fonction pour définir le start stamp personnalisé
  setCustomStart() {
    if (this.mainVideo && this.mainVideo.nativeElement) {
      this.videoService.customStartStamp = Math.round(this.mainVideo.nativeElement.currentTime * 1000); // Convertir en millisecondes
      console.log('Custom start stamp set to:', this.videoService.customStartStamp);
    }
  }

  // Fonction pour définir le end stamp personnalisé
  setCustomEnd() {
    if (this.mainVideo && this.mainVideo.nativeElement) {
      this.videoService.customEndStamp = Math.round(this.mainVideo.nativeElement.currentTime * 1000); // Convertir en millisecondes
      console.log('Custom end stamp set to:', this.videoService.customEndStamp);
    }
  }

  openVideo(shotId : string){
    this.videoService.currentShotID = shotId;
    
    this.service.getShot(shotId)
    .then((shot : any) => {
      this.videoService.currentShot = shot;
      this.videoService.customStartStamp = shot.start_stamp;
      this.videoService.customEndStamp = shot.end_stamp;
      this.setVideoToStartStamp();
    })

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


