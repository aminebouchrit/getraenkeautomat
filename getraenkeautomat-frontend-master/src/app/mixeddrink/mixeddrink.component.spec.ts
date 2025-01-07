import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MixeddrinkComponent } from './mixeddrink.component';

describe('MixeddrinkComponent', () => {
  let component: MixeddrinkComponent;
  let fixture: ComponentFixture<MixeddrinkComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MixeddrinkComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MixeddrinkComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
