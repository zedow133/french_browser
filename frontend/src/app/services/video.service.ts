import { Injectable, signal } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class VideoService {
  public shots = signal<Array<string>>([]) ;            // shots according to the query
  public similarShots = signal<Array<string>>([]);      // shots according to the similar keyframe
  public currentShot: any = null;                       // current shot selected
  public customStartStamp: number = 0;                  // customStartStamp (to be submitted)
  public customEndStamp: number = 0;                    // customEndStamp (to be submitted)
  public currentShotID : string = "";                   // current shotID
  public sessionId : string = "";                       // sessionID (DRES)
  public evaluationId : string = "";                    // evaluationID (DRES)

  constructor() { }

  // Trim the shotID to retrieve the videoID
  trim(shot : string) {
    return shot.split('_')[0]; 
  }
}
