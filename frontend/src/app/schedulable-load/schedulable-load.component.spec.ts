import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SchedulableLoadComponent } from './schedulable-load.component';

describe('SchedulableLoadComponent', () => {
  let component: SchedulableLoadComponent;
  let fixture: ComponentFixture<SchedulableLoadComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SchedulableLoadComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SchedulableLoadComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
