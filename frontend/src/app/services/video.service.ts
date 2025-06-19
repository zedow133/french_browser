import { Injectable, signal } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class VideoService {
  public keyframeNames = signal<Array<string>>([]) ;   // keyframe_names according to the query
  public similarKeyframes = signal<Array<string>>([]);  // keyframes according to the similar keyframe
  public currentShot: any = null;                       // current shot selected
  public customStartStamp: number = 0;                  // customStartStamp (to be submitted)
  public customEndStamp: number = 0;                    // customEndStamp (to be submitted)
  public currentKeyframeName : string = "";             // current keyframe_name
  public sessionId : string = "";                       // sessionID (DRES)
  public evaluationId : string = "";                    // evaluationID (DRES)

  constructor() { }

  // Trim the keyframe_name to retrieve the shotID and the shotID to retrieve the videoID
  trim(str : string) {
    const parts = str.split('_');
    return (parts.slice(0,-1)).join('_'); // '00001_1_0' → '00001_1' → '00001'
  }
}
