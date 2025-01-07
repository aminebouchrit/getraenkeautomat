import { TestBed } from '@angular/core/testing';

import { ReqSendService } from './req.send.service';

describe('ReqSendService', () => {
  let service: ReqSendService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ReqSendService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
