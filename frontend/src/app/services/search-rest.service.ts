import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { lastValueFrom, map } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class SearchRestService {

  constructor(private readonly http: HttpClient) { }

  public async getVideosFromTextQuery() : Promise<Array<string>> {
    return lastValueFrom(this.http.get<Array<string>>("api/videos/shots/query")); 
  }

  public async getVideosFromSimilarity() : Promise<Array<string>> {
    return lastValueFrom(this.http.get<Array<string>>("api/videos/shots/similarity")); 
  }

  public async getVideo(shotID : string) : Promise<Array<string>> {
    return lastValueFrom(this.http.get<Array<string>>("api/videos/shots" + shotID + "")); 
  }

  public async submitVideo() : Promise<Array<string>> {
    return lastValueFrom(this.http.get<Array<string>>("api/videos/shots/submit")); 
  }
  
  

}
