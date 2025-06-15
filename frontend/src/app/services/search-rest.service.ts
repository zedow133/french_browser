import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { last, lastValueFrom, map } from 'rxjs';
import { Shot } from '../models/shot';
import { UserService, LoginRequest, EvaluationClientService, ApiClientAnswer} from '../../../openapi/dres';
import { response } from 'express';

@Injectable({
  providedIn: 'root'
})
export class SearchRestService {

  constructor(private readonly http: HttpClient, private readonly userService : UserService, private readonly evaluationClientService : EvaluationClientService) { }

  public async getVideosFromTextQuery(query : string) : Promise<Array<string>> {
    const apiUrl = '/api/search/text';
    const url = `${apiUrl}?query=${encodeURIComponent(query)}`;
    return lastValueFrom(this.http.get<Array<string>>(url));

    // const namesPromise: Promise<Array<string>> = Promise.resolve(['Sam', 'Alex', 'Leo', 'Leilie', 'Bernard']);
    // return namesPromise;
    
  }

  public async getVideosFromSimilarity(shotID : string) : Promise<Array<string>> {
    const apiUrl = '/api/search/similarity/';
    const url = `${apiUrl}?shot_id=${encodeURIComponent(shotID)}`;
    return lastValueFrom(this.http.get<Array<string>>(url));
  }

  public async getVideo(shotID : string) : Promise<string> {
    return lastValueFrom(this.http.get<string>("api/videos/shots" + shotID + "")); 
  }

  public async login(username : string, password : string) {
    const reponse = this.userService.postApiV2Login({username : username, password : password});
    return lastValueFrom(reponse)
  }

  public async evalId(session : string){
    return lastValueFrom(this.evaluationClientService.getApiV2ClientEvaluationList(session));
  }

  public async submitVideo(session : string, taskName : string, answers : Array<ApiClientAnswer>){

  }
  
  

}
