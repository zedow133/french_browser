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
    // Wait for the video to be loaded
    if (this.mainVideo && this.mainVideo.nativeElement) {
      this.mainVideo.nativeElement.addEventListener('loadedmetadata', () => {
        this.setVideoToStartStamp();
      });
      
      // If video is already loaded
      if (this.mainVideo.nativeElement.readyState >= 1) {
        this.setVideoToStartStamp();
      }
    }
  }

  // Start the video at the start of the shot
  setVideoToStartStamp() {
    if (this.videoService.currentShot && this.videoService.currentShot.start_stamp && this.mainVideo) {
      const startTimeInSeconds = this.videoService.currentShot.start_stamp / 1000;
      this.mainVideo.nativeElement.currentTime = startTimeInSeconds;
    }
  }

  // Submit the video and ask for confirmation
  onSubmitVideoAction() {
    const confirmed = window.confirm('Are you sure you want to submit?');
    if (confirmed) {
      console.log('Submitting...');
      this.service.submitVideo(this.videoService.evaluationId, this.videoService.sessionId, this.videoService.trim(this.videoService.currentShotID), this.videoService.customStartStamp, this.videoService.customEndStamp);
    }
  }

  // Customization of the start and end timestamps for submission 
  setCustomStamp(stamp : string) {
    if (this.mainVideo && this.mainVideo.nativeElement) {
      if(stamp == "start"){
        this.videoService.customStartStamp = Math.round(this.mainVideo.nativeElement.currentTime * 1000); 
        console.log('Custom start stamp set to:', this.videoService.customStartStamp);
      }
      else if (stamp == "end"){
        this.videoService.customEndStamp = Math.round(this.mainVideo.nativeElement.currentTime * 1000);
        console.log('Custom end stamp set to:', this.videoService.customEndStamp);
      }
      else {
        console.error("Invalid stamp")
      }
    }
  }

  // Open Similar Keyframe video
  openVideo(shotId : string){
    this.videoService.currentShotID = shotId;
    
    // Retrieve the selected shot
    this.service.getShot(shotId)
    .then((shot : any) => {
      this.videoService.currentShot = shot;
      this.videoService.customStartStamp = shot.start_stamp;
      this.videoService.customEndStamp = shot.end_stamp;
      this.setVideoToStartStamp();
    })

    console.log("searching for similar keyshots of video : " + shotId);

    // Retrieve the selected similar keyframes
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


