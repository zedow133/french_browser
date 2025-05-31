import { TestBed } from '@angular/core/testing';

import { SearchRestService } from './search-rest.service';

describe('SearchRestService', () => {
  let service: SearchRestService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SearchRestService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
