import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { lastValueFrom, map } from 'rxjs';
import { Shot } from '../models/shot';


@Injectable({
  providedIn: 'root'
})
export class SearchRestService {

  constructor(private readonly http: HttpClient) { }

  public async getVideosFromTextQuery(query : string) : Promise<Array<string>> {
    const apiUrl = '/api/search/text';
    const url = `${apiUrl}?query=${encodeURIComponent(query)}`;
    return lastValueFrom(this.http.get<Array<string>>(url));

    // const namesPromise: Promise<Array<string>> = Promise.resolve(['Sam', 'Alex', 'Leo', 'Leilie', 'Bernard']);
    // return namesPromise;
    
  }

  public async getVideosFromSimilarity(shotID : string) : Promise<Array<string>> {
    return lastValueFrom(this.http.get<Array<string>>("api/videos/shots/similarity" + shotID +"")); 
  }

  public async getVideo(shotID : string) : Promise<string> {
    return lastValueFrom(this.http.get<string>("api/videos/shots" + shotID + "")); 
  }

  public async submitVideo() : Promise<Array<string>> {
    return lastValueFrom(this.http.get<Array<string>>("api/videos/shots/submit")); 
  }
  
  

}
