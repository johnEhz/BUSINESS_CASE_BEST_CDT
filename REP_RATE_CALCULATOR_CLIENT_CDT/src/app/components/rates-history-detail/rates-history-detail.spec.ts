import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RatesHistoryDetail } from './rates-history-detail';

describe('RatesHistoryDetail', () => {
  let component: RatesHistoryDetail;
  let fixture: ComponentFixture<RatesHistoryDetail>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RatesHistoryDetail]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RatesHistoryDetail);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
