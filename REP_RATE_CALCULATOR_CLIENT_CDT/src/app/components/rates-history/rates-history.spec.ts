import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RatesHistory } from './rates-history';

describe('RatesHistory', () => {
  let component: RatesHistory;
  let fixture: ComponentFixture<RatesHistory>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RatesHistory]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RatesHistory);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
