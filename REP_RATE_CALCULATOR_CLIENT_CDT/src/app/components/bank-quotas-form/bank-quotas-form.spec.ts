import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BankQuotasForm } from './bank-quotas-form';

describe('BankQuotasForm', () => {
  let component: BankQuotasForm;
  let fixture: ComponentFixture<BankQuotasForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BankQuotasForm]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BankQuotasForm);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
