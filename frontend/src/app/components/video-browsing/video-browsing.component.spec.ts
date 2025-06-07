import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VideoBrowsingComponent } from './video-browsing.component';

describe('VideoBrowsingComponent', () => {
  let component: VideoBrowsingComponent;
  let fixture: ComponentFixture<VideoBrowsingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [VideoBrowsingComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(VideoBrowsingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
