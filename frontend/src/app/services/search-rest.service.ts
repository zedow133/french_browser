import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { last, lastValueFrom, map } from 'rxjs';
import { Shot } from '../models/shot';
import { UserService, LoginRequest, EvaluationClientService, ApiClientAnswer, SubmissionService, ApiClientSubmission} from '../../../openapi/dres';

@Injectable({
  providedIn: 'root'
})
export class SearchRestService {

  constructor(private readonly http: HttpClient, 
    private readonly userService : UserService, 
    private readonly evaluationClientService : EvaluationClientService,
    private readonly submissionService : SubmissionService) { }

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

  public async submitVideo(evaluationId : string, sessionId : string, mediaName : string, start : number, end : number, text? : string){
    const submission: ApiClientSubmission = {
      answerSets: [
        {
          taskId : "",
          taskName: "",
          answers: [
            {
              text: text,
              mediaItemName: mediaName,
              mediaItemCollectionName: 'IVADL',
              start: start,
              end: end
            }
          ]
        }
      ]
    };
    return lastValueFrom(this.submissionService.postApiV2SubmitByEvaluationId(evaluationId, submission, sessionId))
  }
  
  

}
