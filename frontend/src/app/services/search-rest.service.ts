import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { lastValueFrom, map } from 'rxjs';
import { Shot } from '../models/shot';


@Injectable({
  providedIn: 'root'
})
export class SearchRestService {

  constructor(private readonly http: HttpClient) { }

  public async getVideosFromTextQuery(query : string) : Promise<Array<Shot>> {
    return lastValueFrom(this.http.get<Array<Shot>>("api/videos/shots/" + query +"")); 
  }

  public async getVideosFromSimilarity(shotID : string) : Promise<Array<Shot>> {
    return lastValueFrom(this.http.get<Array<Shot>>("api/videos/shots/similarity" + shotID +"")); 
  }

  public async getVideo(shotID : string) : Promise<Shot> {
    return lastValueFrom(this.http.get<Shot>("api/videos/shots" + shotID + "")); 
  }

  public async submitVideo() : Promise<Array<string>> {
    return lastValueFrom(this.http.get<Array<string>>("api/videos/shots/submit")); 
  }
  
  

}
