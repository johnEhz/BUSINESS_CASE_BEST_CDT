import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RatesManagement } from './rates-management';

describe('RatesManagement', () => {
  let component: RatesManagement;
  let fixture: ComponentFixture<RatesManagement>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RatesManagement]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RatesManagement);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
