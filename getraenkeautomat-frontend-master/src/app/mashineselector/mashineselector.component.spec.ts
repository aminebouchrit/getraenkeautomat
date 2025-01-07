import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MashineselectorComponent } from './mashineselector.component';

describe('MashineselectorComponent', () => {
  let component: MashineselectorComponent;
  let fixture: ComponentFixture<MashineselectorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MashineselectorComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MashineselectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
