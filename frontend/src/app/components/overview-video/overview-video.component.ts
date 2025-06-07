import { CommonModule } from '@angular/common';
import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';

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

  submitText() {
    console.log('Submitted text:', this.query);
  }

  onSubmitVideoAction(action: string) {
    console.log('Video action:', action); // DRES
  }
}


