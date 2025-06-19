import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { lastValueFrom, } from 'rxjs';
import { UserService, EvaluationClientService, SubmissionService, ApiClientSubmission} from '../../../openapi/dres';

@Injectable({
  providedIn: 'root'
})
export class SearchRestService {

  constructor(private readonly http: HttpClient, 
    private readonly userService : UserService, 
    private readonly evaluationClientService : EvaluationClientService,
    private readonly submissionService : SubmissionService) { }

  // Retrieve the keyframes corresponding to the query in similarity order
  public async getVideosFromTextQuery(query : string) : Promise<Array<string>> {
    const apiUrl = '/api/search/text';
    const url = `${apiUrl}?query=${encodeURIComponent(query)}`;
    return lastValueFrom(this.http.get<Array<string>>(url));  
  }

  // Retrieve the keyframes corresponding to the keyframe in similarity order
  public async getVideosFromSimilarity(keyframe_name : string) : Promise<Array<string>> {
    const apiUrl = '/api/search/similarity/';
    const url = `${apiUrl}?keyframe_name=${encodeURIComponent(keyframe_name)}`;
    return lastValueFrom(this.http.get<Array<string>>(url));
  }

  // Retrieve the shot information
  public async getShot(keyframe_name : string) : Promise<string> {
    return lastValueFrom(this.http.get<any>("api/get_shot/" + keyframe_name)); 
  }

  // Login to the Dres server
  public async login(username : string, password : string) {
    const reponse = this.userService.postApiV2Login({username : username, password : password});
    return lastValueFrom(reponse)
  }

  // Retrieve the evaluationID of the current task of the Dres server
  public async evalId(session : string){
    return lastValueFrom(this.evaluationClientService.getApiV2ClientEvaluationList(session));
  }

  // Submit video by constructing the answer
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
