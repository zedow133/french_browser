export class Shot {
    private shotId : string; 
    private source : string
    private startTimeStamp : number; 
    private endTimeStamp : number; 

    public constructor(shot : string, source : string, start : number, end : number) { 
        this.shotId = shot ;
        this.source = source;
        this.startTimeStamp = start;
        this.endTimeStamp = end;
      }

    // Getter
    public getShotId() {
        return this.shotId;
    }

    public getSource() {
        return this.source;
    }

    public getStartTimeStamp() {
        return this.startTimeStamp;
    }

    public getEndTimeStamp() {
        return this.endTimeStamp;
    }
}
