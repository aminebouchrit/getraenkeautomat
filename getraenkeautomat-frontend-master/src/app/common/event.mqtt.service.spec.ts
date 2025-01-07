import { TestBed } from '@angular/core/testing';

import { EventMqttService } from '../common/event.mqtt.service';


describe('EventMqttService', () => {
  let service: EventMqttService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(EventMqttService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
