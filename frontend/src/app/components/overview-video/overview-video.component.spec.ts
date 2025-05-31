import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OverviewVideoComponent } from './overview-video.component';

describe('OverviewVideoComponent', () => {
  let component: OverviewVideoComponent;
  let fixture: ComponentFixture<OverviewVideoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OverviewVideoComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OverviewVideoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
