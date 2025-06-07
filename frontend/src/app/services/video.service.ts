import { Injectable, signal } from '@angular/core';
import { Shot } from '../models/shot';

@Injectable({
  providedIn: 'root'
})
export class VideoService {
  public shots = signal<Array<string>>([]) ;
  public CurrentShot : string = "";

  constructor() { }


}
