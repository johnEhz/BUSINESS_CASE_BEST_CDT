export interface RoiInvestmentSummary {
    amount: string;
    temr_days: number;
    base_days_in_year: number;
}

export interface RoiBankResult {
    consecutive: number;
    id_bank: number;
    qouta: number;
    min_term: number;
    max_term: number;
    min_amount: number;
    max_amount: number;
    last_update: string;
    calculated_interest: string;
}

export interface RoiInterestCalculationResponse {
  investment_summary: RoiInvestmentSummary;
  bank_roi_results: RoiBankResult[];
}