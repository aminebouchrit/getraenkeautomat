import { TestBed } from '@angular/core/testing';

import { ItemscountService } from './itemscount.service';

describe('ItemscountService', () => {
  let service: ItemscountService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ItemscountService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
