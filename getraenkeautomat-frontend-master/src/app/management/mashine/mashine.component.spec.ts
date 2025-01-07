import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MashineComponent } from './mashine.component';

describe('MashineComponent', () => {
  let component: MashineComponent;
  let fixture: ComponentFixture<MashineComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MashineComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MashineComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
