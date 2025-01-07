import { TestBed } from '@angular/core/testing';

import { RecieveService } from './recieve.service';

describe('RecieveService', () => {
  let service: RecieveService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RecieveService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
