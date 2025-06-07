import { Injectable, signal } from '@angular/core';
import { Shot } from '../models/shot';

@Injectable({
  providedIn: 'root'
})
export class VideoService {
  public shots = signal<Array<string>>([]) ;
  public currentShot : string = "";

  constructor() { }

  trim(shot : string) {
    return shot.split('_')[0]; // '00001_1' → '00001'
  }


}
