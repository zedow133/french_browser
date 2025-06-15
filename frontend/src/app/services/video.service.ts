import { Injectable, signal } from '@angular/core';
import { Shot } from '../models/shot';

@Injectable({
  providedIn: 'root'
})
export class VideoService {
  public shots = signal<Array<string>>([]) ;
  public similarShots = signal<Array<string>>([]);
  public currentShot: any = null;
  public customStartStamp: number = 0;
  public customEndStamp: number = 0;
  public currentShotID : string = "";
  public sessionId : string = "";
  public evaluationId : string = "";

  constructor() { }

  trim(shot : string) {
    return shot.split('_')[0]; // '00001_1' → '00001'
  }
}
