import { CommonModule } from '@angular/common';
import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';

@Component({
  selector: 'app-overview-video',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './overview-video.component.html',
  styleUrl: './overview-video.component.css'
})

export class OverviewVideoComponent {
  videoSrc = 'assets/sample-video.mp4'; // Replace with your actual video path
  keyframes: string[] = [];

  submitText(input: string) {
    console.log('Submitted text:', input);
  }

  onSubmitVideoAction(action: string) {
    console.log('Video action:', action);
  }
}


