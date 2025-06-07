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
    
  openVideo(shotId : string) {
    // await this.service.getVideo(shotId) --> videoService.currentShot = ce truc
    this.router.navigate(['video', shotId])
  }

}