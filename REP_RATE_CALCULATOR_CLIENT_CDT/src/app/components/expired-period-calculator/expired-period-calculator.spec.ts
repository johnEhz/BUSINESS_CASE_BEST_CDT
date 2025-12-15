import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExpiredPeriodCalculator } from './expired-period-calculator';

describe('ExpiredPeriodCalculator', () => {
  let component: ExpiredPeriodCalculator;
  let fixture: ComponentFixture<ExpiredPeriodCalculator>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ExpiredPeriodCalculator]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ExpiredPeriodCalculator);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
